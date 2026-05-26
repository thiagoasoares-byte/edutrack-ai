# EduTrack AI

**Project for the Innovation Lab discipline - Faculdade Impacta**
*Student: THIAGO ALVES SOARES*
*2025/2026*

---

## About The Project

EduTrack AI is a sophisticated framework of specialized AI agents designed to orchestrate and accelerate the development of backend applications on the **Xano** platform. This project introduces an agent-based workflow within Visual Studio Code, enabling developers to build, test, and deploy Xano applications with greater efficiency, consistency, and adherence to best practices.

Instead of writing XanoScript code manually, developers interact with a suite of expert agents, each responsible for a specific domain of the Xano ecosystem. This structured approach simplifies complex tasks, from database design to API creation and frontend integration.

## Core Concept

The development process is driven by an orchestrator agent that understands user requirements and delegates implementation tasks to a team of specialized agents. This ensures that each part of the application is built by an expert, following a logical and structured workflow.

The typical development flow is:

1.  **Plan**: Use the `Xano Development Planner` to analyze requirements and create a comprehensive architecture and implementation plan.
2.  **Build**: Delegate tasks to specialized agents to create the necessary components.
3.  **Test**: Use the `Xano Unit Test Writer` to validate functionality and edge cases.
4.  **Integrate**: Use the `Xano Frontend Developer` to connect the backend to a user interface.

## The Agent Team

EduTrack AI is composed of a team of specialized agents, each with a unique role:

-   **`Xano Development Planner`**: The architect. Analyzes requirements, explores the existing codebase, and creates a step-by-step plan for implementation.
-   **`Xano Table Designer`**: The database expert. Designs and modifies database schemas, defines relationships, and sets up indexes for optimal performance.
-   **`Xano Function Writer`**: The logic specialist. Creates reusable business logic, utility helpers, and complex data transformations.
-   **`Xano API Query Writer`**: The interface builder. Creates secure and efficient REST API endpoints (GET, POST, PUT, DELETE) with proper input validation and authentication.
-   **`Xano Task Writer`**: The automation engineer. Builds scheduled background jobs for tasks like data cleanup, report generation, or periodic notifications.
-   **`Xano Addon Writer`**: The data relationship expert. Writes efficient addons to fetch related data (e.g., counts, related records) for database queries.
-   **`Xano AI Builder`**: The AI specialist. Defines custom AI agents, tools, and MCP servers to add intelligent features to the application.
-   **`Xano Frontend Developer`**: The UI/UX integrator. Builds static frontend applications or migrates existing ones (e.g., from Lovable/Supabase) to integrate seamlessly with the Xano backend.
-   **`Xano Unit Test Writer`**: The quality assurance expert. Writes unit and integration tests to ensure all components work as expected.

## Technologies Used

This project leverages a modern, AI-assisted development stack:

-   **Backend Platform**: Xano
-   **Development Environment**: Visual Studio Code
-   **AI Orchestration**: Gemini Code Assist & Custom Agents
-   **API Specification**: OpenSpec
-   **Version Control**: Git & GitHub
-   **Runtime**: Node.js

## Getting Started

To begin working with the EduTrack AI framework, follow these steps:

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    ```
2.  **Open the project in VS Code.**
3.  **Install dependencies** (if any are specified in `package.json`).
    ```sh
    npm install
    ```
4.  **Start with the Planner**: Invoke the `Xano Development Planner` agent to outline your first feature.
    ```
    @workspace /agent Xano Development Planner "I want to build a user authentication system."
    ```
5.  **Follow the Plan**: The planner will provide a handoff to the next appropriate agent (e.g., `Xano Table Designer`) to begin implementation.

## Project Structure

The repository is organized to mirror Xano's architecture, with dedicated directories for each component type:

-   `.github/agents/`: Contains the definitions for all specialized AI agents.
-   `apis/`: Houses the API endpoint queries.
-   `functions/`: Contains reusable functions.
-   `tables/`: Defines the database schemas.
-   `tasks/`: Holds scheduled background tasks.
-   `static/`: For frontend files (HTML, JS, CSS).

## Running the Frontend (Streamlit)

The Streamlit frontend is configured to call your Xano backend via the centralized helper in `utils/api.py`. You can point the app to your deployed Xano instance using environment variables.

- Use a full URL (recommended):

    PowerShell:

    ```powershell
    $Env:API_BASE_URL="https://<your-instance>.n7.xano.io/api"
    $Env:API_TIMEOUT="15"
    streamlit run HOMEPAGE.py
    ```

    Bash (WSL / macOS / Linux):

    ```bash
    export API_BASE_URL="https://<your-instance>.n7.xano.io/api"
    export API_TIMEOUT=15
    streamlit run HOMEPAGE.py
    ```

- Or set the Xano instance id (legacy default format):

    PowerShell:

    ```powershell
    $Env:XANO_INSTANCE="x8ki-letl-twmt"
    streamlit run HOMEPAGE.py
    ```

Notes:
- `API_BASE_URL` overrides `XANO_INSTANCE` when present.
- `API_TIMEOUT` controls HTTP request timeout in seconds (defaults to 15).
- Authentication tokens are stored in Streamlit session state by `utils/auth.py` after login — log in via the app UI to obtain a session token.
- If your Xano instance requires CORS or other settings, configure them in the Xano dashboard.

If you want, I can also add a `.env.example` and a short `README` snippet showing how to store these variables in an env file.

### Default Xano configuration (no .env required)

The frontend is configured to point to the project's Xano workspace by default — you do not need a `.env` file to run the app locally. The base URL is embedded in `utils/api.py` and points to the instance used for this project.

If you prefer an alternative setup (e.g., for CI or another deployment), you can still edit `utils/api.py` to change the `INSTANCE` or `BASE_URL` constants.