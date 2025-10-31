import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm"; // ✅ enables **bold**, lists, tables, etc.
import rehypeRaw from "rehype-raw"; // ✅ allows HTML in markdown

interface ResponseBoxProps {
  text: string;
}

const ResponseBox: React.FC<ResponseBoxProps> = ({ text }) => {
  return (
    <div className="prose prose-sm max-w-none text-foreground">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        components={{
          a: ({ node, ...props }) => (
            <a {...props} className="text-blue-500 hover:underline" target="_blank" rel="noopener noreferrer" />
          ),
          img: ({ node, ...props }) => (
            <img {...props} className="rounded-lg shadow-md max-w-full h-auto my-3" />
          ),
          h3: ({ node, ...props }) => (
            <h3 {...props} className="text-lg font-semibold mt-4 mb-2" />
          ),
          strong: ({ node, ...props }) => (
            <strong {...props} className="font-bold text-primary" />
          ),
          li: ({ node, ...props }) => (
            <li {...props} className="list-disc ml-5" />
          ),
        }}
      >
        {text}
      </ReactMarkdown>
    </div>
  );
};

export default ResponseBox;
