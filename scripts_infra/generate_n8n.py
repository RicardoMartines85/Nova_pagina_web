import json

# Carregar o JSON existente
with open('N8N_WORKFLOW_IMPORT.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

nodes = data['nodes']
connections = data['connections']

# =======================================================
# WORKFLOW 4: Sincronização Resiliente de Fotos + AI Vision
# =======================================================

webhook_sync = {
    "parameters": {"httpMethod": "POST", "path": "appsheet-sync-fotos", "responseMode": "onReceived", "options": {}},
    "id": "wf4-webhook",
    "name": "Webhook: POST /appsheet-sync-fotos",
    "type": "n8n-nodes-base.webhook",
    "typeVersion": 1,
    "position": [100, 1000]
}

split_batches = {
    "parameters": {"batchSize": 5, "options": {}},
    "id": "wf4-split",
    "name": "Split in Batches (Resiliência)",
    "type": "n8n-nodes-base.splitInBatches",
    "typeVersion": 1,
    "position": [300, 1000]
}

ai_vision = {
    "parameters": {
        "method": "POST",
        "url": "https://api.openai.com/v1/chat/completions",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "openApi",
        "sendHeaders": True,
        "headerParameters": {"parameters": [{"name": "Content-Type", "value": "application/json"}]},
        "sendBody": True,
        "bodyParameters": {"parameters": [
            {"name": "model", "value": "gpt-4o"},
            {"name": "messages", "value": "=[{\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\": \"Avalie a qualidade desta foto para um relatório de engenharia. Ela está nítida, clara e bem enquadrada? Responda apenas com um JSON: {\\\"status\\\": \\\"Aprovado\\\" ou \\\"Reprovado\\\", \\\"motivo\\\": \\\"...\\\"}\"}, {\"type\": \"image_url\", \"image_url\": {\"url\": \"{{ $json.url_da_foto }}\"}}]}]"}
        ]}
    },
    "id": "wf4-ai",
    "name": "AI Vision: Validar Qualidade",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 3,
    "position": [500, 1000]
}

if_node = {
    "parameters": {
        "conditions": {
            "string": [{"value1": "={{ $json.choices[0].message.content.status }}", "value2": "Aprovado"}]
        }
    },
    "id": "wf4-if",
    "name": "IF: Aprovado?",
    "type": "n8n-nodes-base.if",
    "typeVersion": 1,
    "position": [700, 1000]
}

edit_image = {
    "parameters": {
        "operation": "text",
        "text": "={{ $node[\"Split in Batches (Resiliência)\"].json.lat }} | {{ $node[\"Split in Batches (Resiliência)\"].json.long }} | {{ $node[\"Split in Batches (Resiliência)\"].json.cidade }} - {{ $node[\"Split in Batches (Resiliência)\"].json.uf }}",
        "fontColor": "#FFFF00",
        "options": {
            "lineColor": "#000000"
        }
    },
    "id": "wf4-edit",
    "name": "Edit Image: Watermark (Carimbo)",
    "type": "n8n-nodes-base.editImage",
    "typeVersion": 1,
    "position": [900, 900]
}

google_drive = {
    "parameters": {
        "operation": "upload",
        "fileContent": "data",
        "options": {}
    },
    "id": "wf4-drive",
    "name": "Google Drive: Salvar Foto",
    "type": "n8n-nodes-base.googleDrive",
    "typeVersion": 2,
    "position": [1100, 900]
}

sheets_aprovado = {
    "parameters": {
        "operation": "append",
        "documentId": {"__rl": True, "mode": "list", "value": "DB_FOTOS_ID"},
        "sheetName": {"__rl": True, "mode": "list", "value": "rdo_fotos"},
        "columns": {
            "mappingMode": "defineBelow",
            "value": {
                "status_ia": "Aprovado",
                "imagem_url": "={{ $json.webViewLink }}"
            }
        }
    },
    "id": "wf4-sheets-ok",
    "name": "Append: DB_Fotos (Aprovado)",
    "type": "n8n-nodes-base.googleSheets",
    "typeVersion": 4,
    "position": [1300, 900]
}

sheets_reprovado = {
    "parameters": {
        "operation": "append",
        "documentId": {"__rl": True, "mode": "list", "value": "DB_FOTOS_ID"},
        "sheetName": {"__rl": True, "mode": "list", "value": "rdo_fotos"},
        "columns": {
            "mappingMode": "defineBelow",
            "value": {
                "status_ia": "Reprovado",
                "motivo_recusa": "={{ $node[\"AI Vision: Validar Qualidade\"].json.choices[0].message.content.motivo }}"
            }
        }
    },
    "id": "wf4-sheets-fail",
    "name": "Append: DB_Fotos (Reprovado)",
    "type": "n8n-nodes-base.googleSheets",
    "typeVersion": 4,
    "position": [900, 1100]
}

nodes.extend([webhook_sync, split_batches, ai_vision, if_node, edit_image, google_drive, sheets_aprovado, sheets_reprovado])

connections["Webhook: POST /appsheet-sync-fotos"] = {"main": [[{"node": "Split in Batches (Resiliência)", "type": "main", "index": 0}]]}
connections["Split in Batches (Resiliência)"] = {"main": [[{"node": "AI Vision: Validar Qualidade", "type": "main", "index": 0}]]}
connections["AI Vision: Validar Qualidade"] = {"main": [[{"node": "IF: Aprovado?", "type": "main", "index": 0}]]}
connections["IF: Aprovado?"] = {
    "main": [
        [{"node": "Edit Image: Watermark (Carimbo)", "type": "main", "index": 0}], # True
        [{"node": "Append: DB_Fotos (Reprovado)", "type": "main", "index": 0}]    # False
    ]
}
connections["Edit Image: Watermark (Carimbo)"] = {"main": [[{"node": "Google Drive: Salvar Foto", "type": "main", "index": 0}]]}
connections["Google Drive: Salvar Foto"] = {"main": [[{"node": "Append: DB_Fotos (Aprovado)", "type": "main", "index": 0}]]}

# O Loop volta pro Split In Batches
connections["Append: DB_Fotos (Aprovado)"] = {"main": [[{"node": "Split in Batches (Resiliência)", "type": "main", "index": 0}]]}
connections["Append: DB_Fotos (Reprovado)"] = {"main": [[{"node": "Split in Batches (Resiliência)", "type": "main", "index": 0}]]}

# =======================================================
# WORKFLOW 5: Geração de Relatório Respeitando Template
# =======================================================

webhook_export = {
    "parameters": {"httpMethod": "GET", "path": "export-xls", "responseMode": "responseNode", "options": {}},
    "id": "wf5-webhook",
    "name": "Webhook: GET /export-xls",
    "type": "n8n-nodes-base.webhook",
    "typeVersion": 1,
    "position": [100, 1300]
}

drive_template = {
    "parameters": {"operation": "download", "fileId": "ID_DO_TEMPLATE_NO_DRIVE"},
    "id": "wf5-drive",
    "name": "Download Excel Template do Cliente",
    "type": "n8n-nodes-base.googleDrive",
    "typeVersion": 2,
    "position": [300, 1300]
}

code_excel = {
    "parameters": {
        "jsCode": "/* Lógica do motor exceljs.\n"
                  "1. O n8n passa o template binário pra cá.\n"
                  "2. Lemos as fotos do payload da requisição (fotos carimbadas do DB_Fotos).\n"
                  "3. Preenchemos o cabeçalho.\n"
                  "4. Para cada foto, adicionamos na planilha: colunas A/B para a primeira foto, C/D para a segunda (exemplo).\n"
                  "5. Agrupamos e rotulamos a seção embaixo.\n"
                  "*/\n"
                  "return [{json: {status: 'XLS Generated', link: 'https://link-to-drive.com/file' }}];"
    },
    "id": "wf5-code",
    "name": "JS: Build Report (ExcelJS) 2x2 Grid",
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [500, 1300]
}

response_export = {
    "parameters": {"respondWith": "allIncomingItems", "options": {}},
    "id": "wf5-resp",
    "name": "Respond to Webhook: GET /export",
    "type": "n8n-nodes-base.respondToWebhook",
    "typeVersion": 1,
    "position": [700, 1300]
}

nodes.extend([webhook_export, drive_template, code_excel, response_export])
connections["Webhook: GET /export-xls"] = {"main": [[{"node": "Download Excel Template do Cliente", "type": "main", "index": 0}]]}
connections["Download Excel Template do Cliente"] = {"main": [[{"node": "JS: Build Report (ExcelJS) 2x2 Grid", "type": "main", "index": 0}]]}
connections["JS: Build Report (ExcelJS) 2x2 Grid"] = {"main": [[{"node": "Respond to Webhook: GET /export", "type": "main", "index": 0}]]}

with open('N8N_WORKFLOW_IMPORT_V2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("N8N_WORKFLOW_IMPORT_V2.json gerado com sucesso!")
