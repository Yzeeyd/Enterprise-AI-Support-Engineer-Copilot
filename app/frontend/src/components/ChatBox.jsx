import {
  useEffect,
  useRef,
  useState
} from "react";

import Message from "./Message";

import {
  sendMessage
} from "../api/chat";


const initialMessages = [
  {
    id: "welcome",
    role: "assistant",

    content:
      "مرحباً، أنا مساعد الدعم المؤسسي. اسألني عن السياسات أو إجراءات الدعم التقني.",

    sources: []
  }
];


function ChatBox() {

  const [
    messages,
    setMessages
  ] = useState(initialMessages);


  const [
    input,
    setInput
  ] = useState("");


  const [
    loading,
    setLoading
  ] = useState(false);


  const [
    error,
    setError
  ] = useState("");


  const bottomRef = useRef(null);


  useEffect(() => {

    bottomRef.current?.scrollIntoView({
      behavior: "smooth"
    });

  }, [
    messages,
    loading
  ]);


  async function submitMessage() {

    const question =
      input.trim();


    if (
      !question ||
      loading
    ) {
      return;
    }


    const userMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: question,
      sources: []
    };


    setMessages(
      current => [
        ...current,
        userMessage
      ]
    );


    setInput("");
    setError("");
    setLoading(true);


    try {

      const result =
        await sendMessage(
          question,
          5
        );


      const assistantMessage = {
        id:
          `assistant-${Date.now()}`,

        role: "assistant",

        content:
          result.answer,

        sources:
          result.sources || []
      };


      setMessages(
        current => [
          ...current,
          assistantMessage
        ]
      );

    } catch (err) {

      console.error(err);

      setError(
        "حدث خطأ أثناء الاتصال بخدمة الذكاء الاصطناعي. حاول مرة أخرى."
      );

    } finally {

      setLoading(false);

    }
  }


  function handleSubmit(event) {

    event.preventDefault();

    submitMessage();
  }


  function handleKeyDown(event) {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      submitMessage();
    }
  }


  return (
    <section className="chat-container">

      <div className="messages">

        {messages.map((message) => (

          <Message
            key={message.id}
            role={message.role}
            content={message.content}
            sources={message.sources}
          />

        ))}


        {loading && (

          <div className="message-row message-assistant-row">

            <div className="assistant-avatar">
              AI
            </div>

            <div className="message message-assistant">

              <div className="thinking">

                <span />
                <span />
                <span />

              </div>

            </div>

          </div>

        )}


        {error && (

          <div className="error-message">
            {error}
          </div>

        )}


        <div ref={bottomRef} />

      </div>


      <form
        className="chat-input-area"
        onSubmit={handleSubmit}
      >

        <textarea
          value={input}

          onChange={
            event =>
              setInput(
                event.target.value
              )
          }

          onKeyDown={
            handleKeyDown
          }

          placeholder="اكتب سؤالك هنا..."

          rows={1}

          disabled={loading}
        />


        <button
          type="submit"

          disabled={
            loading ||
            !input.trim()
          }
        >
          إرسال
        </button>

      </form>


      <div className="input-hint">
        Enter للإرسال • Shift + Enter لسطر جديد
      </div>

    </section>
  );
}


export default ChatBox;