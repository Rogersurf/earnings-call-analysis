export default function ChatMessage({
  role,
  content,
}) {

  const isUser =
    role === "user";

  return (

    <div
      className={`
        rounded-2xl
        p-5
        border
        ${
          isUser
            ? "bg-cyan-500/10 border-cyan-500/20"
            : "bg-[#0b1023] border-cyan-500/10"
        }
      `}
    >

      <div
        className="
          text-xs
          uppercase
          tracking-wider
          mb-2
          text-gray-400
        "
      >

        {isUser
          ? "User"
          : "Semantic Engine"}

      </div>

      <div className="text-gray-200 whitespace-pre-wrap">

        {content}

      </div>

    </div>
  );
}