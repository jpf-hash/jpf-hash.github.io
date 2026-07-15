import type { CollectionEntry } from "astro:content";
import { getSortedPosts } from "./getSortedPosts";
import { postFilter } from "./postFilter";

/**
 * Returns related posts based on tag overlap.
 * Posts are scored by the number of shared tags, then sorted by score descending.
 */
export function getRelatedPosts(
  currentPost: CollectionEntry<"posts">,
  allPosts: CollectionEntry<"posts">[],
  count = 3
): CollectionEntry<"posts">[] {
  const currentTags = new Set(
    currentPost.data.tags.map(t => t.toLowerCase())
  );
  const currentTopic = currentPost.data.topic;

  return getSortedPosts(allPosts)
    .filter(postFilter)
    .filter(p => p.id !== currentPost.id)
    .map(post => ({
      post,
      score:
        post.data.tags.filter(t => currentTags.has(t.toLowerCase())).length +
        Number(Boolean(currentTopic && post.data.topic === currentTopic)),
    }))
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, count)
    .map(item => item.post);
}
