import type { CollectionEntry } from "astro:content";
import { slugifyStr } from "./slugify";

type CategoryCount = {
  category: string;
  slug: string;
  count: number;
};

/** Returns unique categories with post counts, sorted by count descending. */
export function getUniqueCategories(
  posts: CollectionEntry<"posts">[]
): CategoryCount[] {
  const categoryMap = new Map<string, number>();

  for (const post of posts) {
    const category = post.data.category;
    if (category) {
      const slug = slugifyStr(category);
      categoryMap.set(slug, (categoryMap.get(slug) ?? 0) + 1);
    }
  }

  return Array.from(categoryMap.entries())
    .map(([slug, count]) => ({
      category:
        posts.find(p => slugifyStr(p.data.category) === slug)?.data.category ??
        slug,
      slug,
      count,
    }))
    .sort((a, b) => b.count - a.count);
}
