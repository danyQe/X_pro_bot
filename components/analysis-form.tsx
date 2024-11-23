"use client";

import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Loader2 } from "lucide-react";

const formSchema = z.object({
  tweetUrl: z.string().url("Please enter a valid URL"),
});

export default function AnalysisForm() {
  const [isLoading, setIsLoading] = useState(false);
  const [analysis, setAnalysis] = useState<any>(null);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      tweetUrl: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true);
    try {
      // In a real application, this would call your Python backend
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });
      
      const data = await response.json();
      setAnalysis(data);
    } catch (error) {
      console.error("Analysis failed:", error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          <FormField
            control={form.control}
            name="tweetUrl"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Tweet URL</FormLabel>
                <FormControl>
                  <Input placeholder="https://twitter.com/..." {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              "Analyze Tweet"
            )}
          </Button>
        </form>
      </Form>

      {analysis && (
        <Tabs defaultValue="factCheck" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="factCheck">Fact Check</TabsTrigger>
            <TabsTrigger value="sentiment">Sentiment</TabsTrigger>
            <TabsTrigger value="summary">Summary</TabsTrigger>
          </TabsList>
          <TabsContent value="factCheck">
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4">Fact Check Results</h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span>Accuracy Score</span>
                    <span>{analysis.factCheck.score}%</span>
                  </div>
                  <Progress value={analysis.factCheck.score} />
                </div>
                <div className="prose dark:prose-invert">
                  <p>{analysis.factCheck.explanation}</p>
                  {analysis.factCheck.sources && (
                    <div className="mt-4">
                      <h4 className="text-sm font-semibold">Sources:</h4>
                      <ul className="list-disc pl-4">
                        {analysis.factCheck.sources.map((source: string, index: number) => (
                          <li key={index}>{source}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </Card>
          </TabsContent>
          <TabsContent value="sentiment">
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4">Sentiment Analysis</h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span>Sentiment Score</span>
                    <span>{analysis.sentiment.score}</span>
                  </div>
                  <Progress value={(analysis.sentiment.score + 1) * 50} />
                </div>
                <p>{analysis.sentiment.explanation}</p>
              </div>
            </Card>
          </TabsContent>
          <TabsContent value="summary">
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4">Content Summary</h3>
              <p className="text-sm text-muted-foreground mb-4">
                {analysis.summary.text}
              </p>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="text-sm font-semibold mb-2">Key Points</h4>
                  <ul className="list-disc pl-4 text-sm">
                    {analysis.summary.keyPoints.map((point: string, index: number) => (
                      <li key={index}>{point}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="text-sm font-semibold mb-2">Topics</h4>
                  <div className="flex flex-wrap gap-2">
                    {analysis.summary.topics.map((topic: string, index: number) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-secondary text-secondary-foreground rounded-full text-xs"
                      >
                        {topic}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </Card>
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
}