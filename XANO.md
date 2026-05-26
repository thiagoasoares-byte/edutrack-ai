1. The "Cheat Sheet" Strategy (Best for Copilot)
Create a file in your project called xanoscript-rules.md. Whenever you are working on a .xs file, keep this file open in a side tab. Copilot will read it to understand the syntax.

Paste this into your xanoscript-rules.md:

# XanoScript Syntax Rules
- **Types**: Use `text` (not string), `int` (not integer), `bool` (not boolean), `decimal` (not float).
- **Inputs**: Always access inputs via `$input.variable_name`.
- **Conditionals**: Use `elseif` (one word), never `else if`.
- **Comments**: Only use `//`. Never use `#` or `/* */`.
- **Blocks**: Properties inside blocks (like `db.query`) use `=` and no commas. Object literals (like `data = { ... }`) use `:` and require commas.
- **Filters**: When using filters in an expression (e.g., in an `if` statement), always wrap the filtered part in parentheses: `if (($var|strlen) > 0)`.
- **API Requests**: Use `params` for the request body, never `body`.
2. Prompting Tips for Better Code
When asking Copilot to generate code, be very specific about Xano-specific patterns. Instead of saying "Create a login API," use a prompt like this:

"Write a XanoScript query for a login endpoint. Use the user table for auth. Use text and password types in the input block. Use security.check_password in the stack. Remember that XanoScript uses text instead of string and require $input. for all inputs."

3. Keep "Reference Files" Open
Copilot uses "Neighboring Tabs" to understand context. If you are writing a new API for the subjects table, make sure /table/subjects.xs is open in another tab. Copilot will see the schema and know exactly which fields (like user_id or teacher) it should be using in the code.

4. Use the "Strict Typing" Instruction
If Copilot keeps hallucinating JavaScript types (like let, const, or string), add this line to your prompt:

"Strictly use XanoScript types: text, int, decimal, bool, timestamp. Do not use JavaScript keywords."

5. Correcting Mistakes
If Copilot makes a mistake (like using else if), don't just fix it manually. Highlight the code and tell Copilot:

"In XanoScript, 'else if' must be written as 'elseif'. Please fix this and check for other syntax errors."

Summary for your Copilot Custom Instructions:
If you use GitHub Copilot Custom Instructions (the .github/copilot-instructions.md file), add this:

Always write code in XanoScript (.xs). 
XanoScript specific rules:
1. No 'string' type, use 'text'. 
2. No 'integer' type, use 'int'.
3. Use 'elseif' instead of 'else if'.
4. Variable access: $input.var for inputs, $var for local variables.
5. All database calls (db.query, db.get) must include the table name in quotes: db.query "table_name".
6. Wrap filtered expressions in parentheses: ($var|filter).
