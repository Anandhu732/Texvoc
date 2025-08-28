'use client';

import { useState, useRef, useCallback, useEffect } from 'react';
import { Upload, Mic, Download, Play, Pause, Volume2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

interface Voice {
  id: string;
  name: string;
}

export default function Home() {
  const [text, setText] = useState('');
  const [selectedVoice, setSelectedVoice] = useState<string>('');
  const [voices, setVoices] = useState<Voice[]>([]);
  const [audioUrl, setAudioUrl] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Fetch voices on component mount
  useEffect(() => {
    fetchVoices();
  }, []);

  const fetchVoices = async () => {
    try {
      const response = await fetch('http://localhost:8000/voices');
      if (response.ok) {
        const voiceList = await response.json();
        setVoices(voiceList);
      }
    } catch (error) {
      console.error('Failed to fetch voices:', error);
    }
  };

  const handleSynthesize = async () => {
    if (!text.trim() || !selectedVoice) return;

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/synthesize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text.trim(),
          voice_id: selectedVoice,
        }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setAudioUrl(url);
      }
    } catch (error) {
      console.error('Failed to synthesize speech:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = useCallback(async (file: File) => {
    if (!file.name.endsWith('.wav')) {
      alert('Please upload a WAV file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/voices', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        fetchVoices(); // Refresh voice list
      }
    } catch (error) {
      console.error('Failed to upload voice:', error);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  }, [handleFileUpload]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
  }, []);

  const togglePlayback = () => {
    if (!audioRef.current) return;

    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  const downloadAudio = () => {
    if (!audioUrl) return;

    const a = document.createElement('a');
    a.href = audioUrl;
    a.download = 'synthesized-speech.wav';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/10">
      {/* Navbar */}
      <nav className="backdrop-blur-md bg-transparent border-b border-white/5">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-primary to-primary/70 rounded-lg flex items-center justify-center animate-float">
                <Volume2 className="w-5 h-5 text-primary-foreground" />
              </div>
              <h1 className="text-2xl font-bold gradient-text">TxVoc</h1>
            </div>
            <div className="text-sm text-muted-foreground">
              Text-to-Speech Synthesis
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-12">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Header */}
          <div className="text-center space-y-4">
            <h2 className="text-4xl md:text-6xl font-bold gradient-text">
              Transform Text to Speech
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Convert your text into natural-sounding speech with our advanced synthesis technology
            </p>
          </div>

          {/* Text Input Card */}
          <Card className="glass-effect border-primary/20">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Mic className="w-5 h-5 text-primary" />
                <span>Enter Your Text</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Type or paste your text here..."
                className="w-full h-32 px-4 py-3 bg-background/50 border border-border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200"
              />

              {/* Voice Selection */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">
                  Select Voice
                </label>
                <Select value={selectedVoice} onValueChange={setSelectedVoice}>
                  <SelectTrigger className="bg-background/50 border-border">
                    <SelectValue placeholder="Choose a voice..." />
                  </SelectTrigger>
                  <SelectContent>
                    {voices.map((voice) => (
                      <SelectItem key={voice.id} value={voice.id}>
                        {voice.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Synthesize Button */}
              <Button
                onClick={handleSynthesize}
                disabled={!text.trim() || !selectedVoice || isLoading}
                className="w-full bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 transition-all duration-200"
                size="lg"
              >
                {isLoading ? (
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin" />
                    <span>Synthesizing...</span>
                  </div>
                ) : (
                  <>
                    <Volume2 className="w-4 h-4 mr-2" />
                    Generate Speech
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Voice Upload Card */}
          <Card className="glass-effect border-secondary/20">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Upload className="w-5 h-5 text-secondary" />
                <span>Upload Voice Sample</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div
                className={`drag-area border-2 border-dashed rounded-lg p-8 text-center transition-all duration-300 cursor-pointer ${
                  dragOver
                    ? 'border-primary bg-primary/10 scale-105'
                    : 'border-border hover:border-primary/50'
                }`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onClick={() => fileInputRef.current?.click()}
              >
                <Upload className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-lg font-medium text-foreground mb-2">
                  Drop your WAV file here
                </p>
                <p className="text-muted-foreground">
                  or click to browse files
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".wav"
                  className="hidden"
                  onChange={(e) => {
                    const file = e.target.files?.[0];
                    if (file) handleFileUpload(file);
                  }}
                />
              </div>
            </CardContent>
          </Card>

          {/* Audio Player Card */}
          {audioUrl && (
            <Card className="glass-effect border-accent/20">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Play className="w-5 h-5 text-accent" />
                  <span>Generated Audio</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-center space-x-4">
                  <Button
                    onClick={togglePlayback}
                    variant="outline"
                    size="lg"
                    className="bg-background/50 border-border hover:bg-background/70"
                  >
                    {isPlaying ? (
                      <Pause className="w-5 h-5" />
                    ) : (
                      <Play className="w-5 h-5" />
                    )}
                  </Button>

                  <Button
                    onClick={downloadAudio}
                    variant="outline"
                    size="lg"
                    className="bg-background/50 border-border hover:bg-background/70"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Download
                  </Button>
                </div>

                <audio
                  ref={audioRef}
                  src={audioUrl}
                  onEnded={() => setIsPlaying(false)}
                  className="w-full"
                  controls
                />
              </CardContent>
            </Card>
          )}
        </div>
      </main>
    </div>
  );
}
