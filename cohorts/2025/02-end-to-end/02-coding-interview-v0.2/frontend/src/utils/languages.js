/**
 * Language configurations for the code editor
 * Centralized language support information
 */

/**
 * Supported programming languages
 */
export const SUPPORTED_LANGUAGES = {
  PYTHON: 'python',
  JAVASCRIPT: 'javascript',
};

/**
 * Language display names
 */
export const LANGUAGE_NAMES = {
  [SUPPORTED_LANGUAGES.PYTHON]: 'Python',
  [SUPPORTED_LANGUAGES.JAVASCRIPT]: 'JavaScript',
};

/**
 * Default code snippets for each language
 */
export const DEFAULT_CODE = {
  [SUPPORTED_LANGUAGES.PYTHON]: `# Write your Python code here
def hello():
    print("Hello, World!")

hello()
`,
  [SUPPORTED_LANGUAGES.JAVASCRIPT]: `// Write your JavaScript code here
function hello() {
  console.log("Hello, World!");
}

hello();
`,
};

/**
 * Get list of supported languages for UI selection
 */
export function getSupportedLanguages() {
  return Object.values(SUPPORTED_LANGUAGES).map(lang => ({
    value: lang,
    label: LANGUAGE_NAMES[lang],
  }));
}
