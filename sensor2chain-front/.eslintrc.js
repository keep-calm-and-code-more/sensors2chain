module.exports = {
    extends: [
        "./node_modules/react-redux-typescript-scripts/eslint.js",
        "prettier",
         "react-app"
        // "./node_modules/react-redux-typescript-scripts/eslint-prettier.js", // optional
    ],
    plugins: ["mui-unused-classes"],
    rules: {
        'mui-unused-classes/unused-classes': 1
    },
    overrides: [
        {
            files: ["*.js"],
            rules: {
                "@typescript-eslint/explicit-module-boundary-types": "off",
                "@typescript-eslint/no-var-requires": "off",
            },
        },
    ],
};
