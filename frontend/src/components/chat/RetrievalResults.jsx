export default function RetrievalResults({
  results,
}) {

  if (!results?.length) {

    return (

      <div
        className="
          text-gray-500
          text-sm
        "
      >
        No semantic results.
      </div>
    );
  }

  return (

    <div className="space-y-4">

      {results.map((result, idx) => (

        <div
          key={idx}
          className="
            bg-[#0b1023]
            border
            border-cyan-500/10
            rounded-2xl
            p-5
            space-y-3
          "
        >

          <div className="flex justify-between">

            <div>

              <div className="text-cyan-400 font-bold">

                {result.company}

              </div>

              <div className="text-gray-500 text-sm">

                {result.ticker}

              </div>

            </div>

            <div className="text-green-400">

              {(result.similarity * 100)
                .toFixed(1)}%

            </div>

          </div>

          <div className="text-gray-300 text-sm leading-relaxed">

            {result.chunk_text}

          </div>

        </div>

      ))}

    </div>
  );
}