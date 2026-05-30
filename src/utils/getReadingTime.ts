/**
 * Estimate reading time in minutes for a given text.
 * Uses an average reading speed of 400 characters per minute for CJK content,
 * and 200 words per minute for Latin content.
 */
export function getReadingTime(text: string): number {
  if (!text) return 1;

  // Count CJK characters (Chinese/Japanese/Korean)
  const cjkChars = (text.match(/[一-鿿㐀-䶿豈-﫿]/g) || []).length;

  // Count Latin words (everything that's not CJK or whitespace)
  const latinText = text.replace(/[一-鿿㐀-䶿豈-﫿]/g, "");
  const latinWords = latinText.split(/\s+/).filter(w => w.length > 0).length;

  // CJK: ~400 chars/min, Latin: ~200 words/min
  const cjkMinutes = cjkChars / 400;
  const latinMinutes = latinWords / 200;

  const totalMinutes = cjkMinutes + latinMinutes;
  return Math.max(1, Math.ceil(totalMinutes));
}
