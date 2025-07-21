"use client";
import { useState } from "react";
import { Divider } from "@nextui-org/divider";
import { Progress } from "@nextui-org/progress";
import { Chip } from "@nextui-org/chip";
import { Card, CardHeader, CardBody, CardFooter } from "@nextui-org/card";

// Styled Button
const Button = ({ children, className = "", ...props }) => (
  <button
    className={`px-4 py-2 rounded-md font-medium bg-pink-600 text-white hover:bg-pink-700 transition ${className}`}
    {...props}
  >
    {children}
  </button>
);

// Styled Input
const Input = ({ type = "text", ...props }) => (
  <input
    type={type}
    className="w-full px-4 py-2 border border-pink-300 rounded-md focus:outline-none focus:border-pink-500 bg-white text-black"
    {...props}
  />
);

export default function AIGen() {
  const [topic, setTopic] = useState("");
  const [duration, setDuration] = useState(60);
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState<string| null>(null);
  const [error, setError] = useState<string| null>(null);

  const suggestions = [
    "news topic about the world",
    "quiz about country capitals",
    "text message between two friends",
    "rank fast food",
    "would you rather about food",
  ];

  async function generateVideo() {
    setError(null);
    setVideoUrl(null);

    if (!topic.trim()) {
      setError("Please enter a topic.");
      return;
    }

    if (duration <= 0) {
      setError("Duration must be > 0.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/generate-video", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, duration }),
      });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Server error");
      }
      if (!data.video_url) {
        throw new Error("No video URL returned");
      }
      setVideoUrl(`http://localhost:8000/${data.video_url}`);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  // Loading state
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-screen gap-4">
        <Progress isIndeterminate size="md" />
        <p>Generating your video… please wait</p>
      </div>
    );
  }

  // Success state
  if (videoUrl) {
    return (
      <div className="flex flex-col items-center justify-center h-screen gap-6 px-4">
        <h2 className="text-2xl font-bold text-pink-600">Your Video Is Ready!</h2>
        <video
          controls
          className="w-full max-w-2xl rounded shadow"
          src={videoUrl}
        />
        <Button onClick={() => window.location.reload()}>Generate Another</Button>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-screen gap-4 px-4">
        <h2 className="text-2xl font-bold text-red-600">Error</h2>
        <p className="text-red-600">{error}</p>
        <Button onClick={() => window.location.reload()}>Try Again</Button>
      </div>
    );
  }

  // Default form
  return (
    <div className="flex flex-col items-center min-h-screen py-16 px-4 bg-gradient-to-br from-pink-50 via-white to-purple-50">
      <div className="w-full max-w-lg">
        <Card className="bg-white/80 backdrop-blur-sm">
          <CardHeader className="text-center py-8">
            <h1 className="text-3xl font-bold text-pink-600">Generate AI Video</h1>
            <Divider className="my-4 bg-pink-300" />
          </CardHeader>

          <CardBody className="space-y-6">
            <div>
              <label className="block font-medium text-gray-700 mb-1">Topic</label>
              <Input
                placeholder="Enter topic…"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
              />
            </div>
            <div>
              <label className="block font-medium text-gray-700 mb-1">
                Duration (seconds)
              </label>
              <Input
                type="number"
                value={duration}
                onChange={(e) => setDuration(Number(e.target.value))}
              />
            </div>

            <div className="flex flex-wrap gap-2">
              {suggestions.map((s) => (
                <Chip
                  key={s}
                  variant="bordered"
                  className="cursor-pointer text-pink-600 border-pink-300 hover:bg-pink-100 text-xs"
                  onClick={() => setTopic(s)}
                >
                  {s}
                </Chip>
              ))}
            </div>

            <Divider />

            <Button
              className={`w-full py-3 ${!topic.trim() ? "opacity-70" : ""}`}
              onClick={generateVideo}
              disabled={!topic.trim()}
            >
              {topic.trim() ? "Render Video" : "Enter a topic first"}
            </Button>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
