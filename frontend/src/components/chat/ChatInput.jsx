import { useState } from "react";

export default function ChatInput({
  onSend,
  loading,
}) {

  const [query, setQuery] =
    useState("");

  async function handleSubmit(e) {

    e.preventDefault();

    if (!query.trim()) return;

    await onSend(query);

    setQuery("");
  }

  return (

    <form
      onSubmit={handleSubmit}
      className="
        flex
        gap-4
        w-full
      "
    >

      <input
        type="text"
        placeholder="
          Ask about semantic propagation...
        "
        value={query}
        onChange={(e) =>
          setQuery(e.target.value)
        }
        className="
          flex-1
          bg-[#0b1023]
          border
          border-cyan-500/10
          rounded-2xl
          px-5
          py-4
          text-white
          outline-none
          focus:border-cyan-400/30
        "
      />

      <button
        type="submit"
        disabled={loading}
        className="
          px-6
          py-4
          rounded-2xl
          bg-cyan-500
          text-black
          font-bold
          hover:scale-105
          transition
        "
      >

        {loading
          ? "Thinking..."
          : "Send"}

      </button>

    </form>
  );
}