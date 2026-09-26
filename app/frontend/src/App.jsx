import ChatBox from "./components/ChatBox";


function App() {
  return (
    <div className="app">

      <header className="header">

        <div className="brand">

          <div className="brand-icon">
            AI
          </div>

          <div>
            <h1>
              Enterprise AI Support Copilot
            </h1>

            <p>
              Hybrid RAG • OpenSearch • Ollama
            </p>
          </div>

        </div>

        <div className="status">

          <span className="status-dot" />

          <span>
            Online
          </span>

        </div>

      </header>


      <main className="main">

        <section className="hero">

          <span className="hero-badge">
            Enterprise Knowledge Assistant
          </span>

          <h2>
            كيف يمكنني مساعدتك؟
          </h2>

          <p>
            اسأل عن سياسات الشركة،
            الدعم التقني، كلمات المرور
          </p>

        </section>


        <ChatBox />

      </main>


      <footer className="footer">
        Enterprise AI Support Engineer Copilot
        {" • "}
        Hybrid RAG
      </footer>

    </div>
  );
}


export default App;