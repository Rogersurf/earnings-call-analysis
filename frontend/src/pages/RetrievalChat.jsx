import { useState } from "react";

import ChatInput from
  "../components/chat/ChatInput";

import ChatMessage from
  "../components/chat/ChatMessage";

import RetrievalResults from
  "../components/chat/RetrievalResults";

import {
  searchSemantic
} from "../services/retrievalService";

export default function RetrievalChat() {

  const [messages, setMessages] =
    useState([]);

  const [results, setResults] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  async function handleSend(query) {

    setLoading(true);

    setMessages((prev) => [

      ...prev,

      {
        role: "user",
        content: query,
      }

    ]);

    const data =
      await searchSemantic(query);

    if (data?.results) {

      setResults(data.results);

      setMessages((prev) => [

        ...prev,

        {
          role: "assistant",
          content:
            `Retrieved ${data.results.length} semantic matches.`,
        }

      ]);
    }

    setLoading(false);
  }

  return (

    <div
      className="
        min-h-screen
        bg-[#050816]
        text-white
        p-8
      "
    >

      <div
        className="
          max-w-5xl
          mx-auto
          space-y-6
        "
      >

        <div>

          <h1 className="text-4xl font-bold">

            Semantic Retrieval Chat

          </h1>

          <p className="text-gray-400 mt-2">

            Explore semantic propagation
            across earnings calls.

          </p>

        </div>

        <ChatInput
          onSend={handleSend}
          loading={loading}
        />

        <div className="space-y-4">

          {messages.map((msg, idx) => (

            <ChatMessage
              key={idx}
              role={msg.role}
              content={msg.content}
            />

          ))}

        </div>

        <RetrievalResults
          results={results}
        />

      </div>

    </div>
  );
}