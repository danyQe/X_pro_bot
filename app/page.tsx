import { Terminal } from "lucide-react";
import AnalysisForm from "@/components/analysis-form";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)]">
      <div className="max-w-3xl w-full space-y-8">
        <div className="text-center">
          <div className="flex justify-center mb-4">
            <Terminal className="h-12 w-12 text-primary" />
          </div>
          <h1 className="text-4xl font-bold tracking-tight">Truth Terminal</h1>
          <p className="mt-4 text-lg text-muted-foreground">
            AI-powered analysis for Twitter content verification, sentiment analysis, and summarization
          </p>
        </div>
        
        <AnalysisForm />
      </div>
    </div>
  );
}