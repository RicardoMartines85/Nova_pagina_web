import { createServerFn } from "@tanstack/react-start";
import * as fs from "fs";
import * as path from "path";

// Tipagem baseada no que salvamos no N8N
interface Post {
  slug?: string;
  title: string;
  excerpt: string;
  content?: string;
  meta?: string;
  link?: string;
  image?: string;
  date?: string;
}

const getPostsFilePath = () => {
  const isProd = process.env.NODE_ENV === "production";
  const dataDir = isProd
    ? path.join(process.cwd(), "dist", "client", "blog_data")
    : path.join(process.cwd(), "public", "blog_data");
  return path.join(dataDir, "posts.json");
};

export const getPostsAdmin = createServerFn({ method: "GET" }).handler(async () => {
  try {
    const filePath = getPostsFilePath();
    if (!fs.existsSync(filePath)) {
      return { posts: [] as Post[] };
    }
    const data = JSON.parse(fs.readFileSync(filePath, "utf-8"));
    // O N8N pode salvar como array direto ou num objeto { posts: [] }
    const postsArray = Array.isArray(data) ? data : data.posts || [];
    return { posts: postsArray as Post[] };
  } catch (error) {
    console.error("Erro ao listar posts admin:", error);
    return { posts: [] as Post[] };
  }
});

export const deletePost = createServerFn({ method: "POST" })
  .inputValidator((data: { slug: string }) => data)
  .handler(async ({ data }) => {
    try {
      const filePath = getPostsFilePath();
      if (!fs.existsSync(filePath)) {
        return { success: false, error: "Arquivo de posts não encontrado" };
      }

      const fileData = JSON.parse(fs.readFileSync(filePath, "utf-8"));
      let postsArray = Array.isArray(fileData) ? fileData : fileData.posts || [];

      // Filtra removendo o post desejado
      const initialLength = postsArray.length;
      postsArray = postsArray.filter((p: Post) => p.slug !== data.slug);

      if (postsArray.length === initialLength) {
        return { success: false, error: "Post não encontrado pelo slug fornecido" };
      }

      // Salva de volta no arquivo
      fs.writeFileSync(filePath, JSON.stringify(postsArray, null, 2));
      return { success: true };
    } catch (error) {
      console.error("Erro ao deletar post:", error);
      return { success: false, error: "Erro interno no servidor" };
    }
  });
