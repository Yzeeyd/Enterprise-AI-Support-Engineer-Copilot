import Sources from "./Sources";


function Message({
  role,
  content,
  sources = []
}) {

  const isUser =
    role === "user";


  return (
    <div
      className={
        `message-row ${
          isUser
            ? "message-user-row"
            : "message-assistant-row"
        }`
      }
    >

      {!isUser && (

        <div className="assistant-avatar">
          AI
        </div>

      )}


      <div
        className={
          `message ${
            isUser
              ? "message-user"
              : "message-assistant"
          }`
        }
      >

        <div
          className="message-content"
          dir="auto"
        >
          {content}
        </div>


        {!isUser && (

          <Sources
            sources={sources}
          />

        )}

      </div>

    </div>
  );
}


export default Message;