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
  tweet: z.string().min(1, "Please enter a tweet text"),
});

export default function AnalysisForm() {
  const [isLoading, setIsLoading] = useState(false);
  const [activeAnalysis, setActiveAnalysis] = useState<"sentiment" | "facts" | "viral" | null>(null);
  const [analysisResults, setAnalysisResults] = useState<{
    sentiment?: { sentiment_description: string };
    facts?: { Fact_description: string };
    viral?: { viral_tweets: string[] };
  }>({});

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      tweet: "",
    },
  });

  // components/analysis-form.tsx
  // Update the analyzeTweet function
  
  const analyzeTweet = async (type: "sentiment" | "facts" | "viral") => {
    setIsLoading(true);
    setActiveAnalysis(type);
    
    try {
      let response;
      if (type === "viral") {
        response = await fetch("/api/viral");
      } else {
        response = await fetch(`/api/${type}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ tweet: form.getValues("tweet") }),
        });
      }
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Analysis failed');
      }
      
      const data = await response.json();
      setAnalysisResults(prev => ({ ...prev, [type]: data }));
    } catch (error) {
      console.error(`${type} analysis failed:`, error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <Form {...form}>
        <form className="space-y-4">
          <FormField
            control={form.control}
            name="tweet"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Tweet Text</FormLabel>
                <FormControl>
                  <Input placeholder="Enter tweet content..." {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <div className="flex gap-4">
            <Button 
              type="button" 
              className="flex-1"
              disabled={isLoading}
              onClick={() => analyzeTweet("sentiment")}
            >
              {isLoading && activeAnalysis === "sentiment" ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Analyzing...
                </>
              ) : (
                "Analyze Sentiment"
              )}
            </Button>
            <Button 
              type="button"
              className="flex-1"
              disabled={isLoading}
              onClick={() => analyzeTweet("facts")}
            >
              {isLoading && activeAnalysis === "facts" ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Checking Facts...
                </>
              ) : (
                "Check Facts"
              )}
            </Button>
            <Button 
              type="button"
              className="flex-1"
              disabled={isLoading}
              onClick={() => analyzeTweet("viral")}
            >
              {isLoading && activeAnalysis === "viral" ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generating...
                </>
              ) : (
                "Generate Viral Tweets"
              )}
            </Button>
          </div>
        </form>
      </Form>

      {Object.keys(analysisResults).length > 0 && (
        <Tabs defaultValue={activeAnalysis || "sentiment"} className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="sentiment">Sentiment</TabsTrigger>
            <TabsTrigger value="facts">Fact Check</TabsTrigger>
            <TabsTrigger value="viral">Viral Tweets</TabsTrigger>
          </TabsList>
          
          <TabsContent value="sentiment">
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4">Sentiment Analysis</h3>
              {analysisResults.sentiment && (
                <p className="text-sm text-muted-foreground">
                  {analysisResults.sentiment.sentiment_description}
                </p>
              )}
            </Card>
          </TabsContent>
          
          <TabsContent value="facts">
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4">Fact Check Results</h3>
              {analysisResults.facts && (
                <p className="text-sm text-muted-foreground">
                  {analysisResults.facts.Fact_description}
                </p>
              )}
            </Card>
          </TabsContent>
          
          <TabsContent value="viral">
            <Card className="p-6">
              <h3 className="text-lg font-semibold mb-4">Viral Tweet Suggestions</h3>
              {analysisResults.viral && (
                <div className="space-y-4">
                  {analysisResults.viral.viral_tweets.map((tweet, index) => (
                    <div 
                      key={index}
                      className="p-4 bg-secondary rounded-lg"
                    >
                      <p className="text-sm">{tweet}</p>
                    </div>
                  ))}
                </div>
              )}
            </Card>
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
}