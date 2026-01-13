import { useEffect, useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  ArrowRight,
  Sparkles,
  MapPin,
  Star,
  CheckCircle2,
  AlertTriangle,
  Calendar,
  IndianRupee,
  BookOpen,
  Rocket,
  Heart,
  Shield,
  Info,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import logo from '@/assets/delhi-career-navigator-logo.png';
import dashboardBgDesktop from '@/assets/dashboard-bg-desktop.png';
import dashboardBgMobile from '@/assets/dashboard-bg-mobile.png';
import { formDataSchema, safeDisplayValue, type ValidatedFormData } from '@/lib/formValidation';

interface ApiRecommendation {
  rank: number;
  pathway_name: string;
  description: string;
  why_recommended: string;
  fit_score: string;
  required_skills: string[];
  estimated_salary: string;
  growth_prospects: string;
  considerations: string[];
  next_steps: string[];
}

interface ApiResponse {
  user_name: string;
  preferred_language: string;
  recommendations: ApiRecommendation[];
  source?: string;
  disclaimer?: string;
  demo_mode?: boolean;
}

const LS_FORM_KEY = 'dcn_formData';
const LS_REC_KEY = 'dcn_recommendations';

const Dashboard = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // Try navigation state first, then localStorage
  const apiData: ApiResponse | undefined = useMemo(() => {
    if (location.state?.recommendations) return location.state.recommendations as ApiResponse;

    try {
      const stored = localStorage.getItem(LS_REC_KEY);
      if (stored) return JSON.parse(stored) as ApiResponse;
    } catch (err) {
      console.warn('Unable to parse stored recommendations', err);
    }
    return undefined;
  }, [location.state]);

  const validatedFormData = useMemo((): ValidatedFormData | null => {
    if (location.state?.formData) {
      const res = formDataSchema.safeParse(location.state.formData);
      if (res.success) return res.data;
    }
    try {
      const stored = localStorage.getItem(LS_FORM_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        const res = formDataSchema.safeParse(parsed);
        if (res.success) return res.data;
      }
    } catch (err) {
      console.warn('Unable to parse stored form data', err);
    }
    return null;
  }, [location.state]);

  const [selected, setSelected] = useState<ApiRecommendation | null>(null);

  useEffect(() => {
    if (!apiData?.recommendations?.length) {
      navigate('/get-started');
    }
  }, [apiData, navigate]);

  if (!apiData?.recommendations?.length) {
    return null;
  }

  const firstName =
    (apiData.user_name || validatedFormData?.name || 'there')
      .split(' ')[0];

  return (
    <div className="min-h-screen relative overflow-hidden bg-gradient-to-br from-slate-50 via-blue-50/30 to-violet-50/20">
      {/* Backgrounds */}
      <div className="absolute inset-0">
        <div className="hidden md:block absolute inset-0 opacity-40" style={{ backgroundImage: `url(${dashboardBgDesktop})`, backgroundSize: 'cover', backgroundPosition: 'center' }} />
        <div className="md:hidden absolute inset-0 opacity-40" style={{ backgroundImage: `url(${dashboardBgMobile})`, backgroundSize: 'cover', backgroundPosition: 'center' }} />
      </div>
      <div className="absolute top-20 right-10 w-72 h-72 bg-primary/5 rounded-full blur-3xl" />
      <div className="absolute bottom-20 left-10 w-96 h-96 bg-violet-500/5 rounded-full blur-3xl" />

      {/* Header */}
      <header className="container mx-auto px-4 py-6 flex items-center justify-between relative z-10">
        <motion.button
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          onClick={() => navigate('/')}
          className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors group bg-white/70 backdrop-blur-sm px-4 py-2 rounded-full border border-border/50 shadow-sm"
        >
          <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
          <span className="font-medium text-sm">Back to Home</span>
        </motion.button>

        <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}>
          <img src={logo} alt="Delhi Career Navigator" className="h-10 w-auto object-contain" />
        </motion.div>
      </header>

      <main className="container mx-auto px-4 pb-16 relative z-10">
        {/* Intro */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-10"
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.1 }}
            className="inline-flex items-center gap-2 bg-gradient-to-r from-primary/10 to-violet-500/10 text-primary px-5 py-2 rounded-full text-sm font-medium mb-4 border border-primary/20"
          >
            <Sparkles className="w-4 h-4" />
            <span>AI-Powered Career Guidance</span>
          </motion.div>

          <h1 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-2">
            Hey {firstName}! 👋
          </h1>
          <p className="text-muted-foreground text-base md:text-lg max-w-2xl mx-auto leading-relaxed">
            Here are your personalized career pathways based on your profile and goals.
          </p>
          {apiData.disclaimer && (
            <div className="mt-4 inline-flex items-start gap-2 text-xs text-muted-foreground bg-white/70 backdrop-blur-sm px-3 py-2 rounded-lg border border-border/60">
              <Shield className="w-4 h-4 text-primary mt-0.5" />
              <span>{apiData.disclaimer}</span>
            </div>
          )}
        </motion.div>

        {/* Cards */}
        <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {apiData.recommendations
            .slice()
            .sort((a, b) => a.rank - b.rank)
            .map((rec, index) => (
              <motion.div
                key={rec.rank}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.12 * index }}
                className="group"
              >
                <Card className="bg-white/85 backdrop-blur-sm rounded-2xl overflow-hidden hover:shadow-xl hover:shadow-primary/10 transition-all duration-400 hover:-translate-y-1.5 h-full border border-border/60 relative">
                  {rec.rank === 1 && (
                    <div className="absolute top-4 right-4 z-10">
                      <div className="bg-gradient-to-r from-emerald-500 to-teal-500 text-white text-xs font-bold px-3 py-1.5 rounded-full shadow-lg shadow-emerald-500/30 flex items-center gap-1.5">
                        <Star className="w-3 h-3 fill-white" />
                        Best Match
                      </div>
                    </div>
                  )}

                  <div className="bg-gradient-to-br from-primary to-violet-600 p-6 text-white">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-display text-xl font-bold">{rec.pathway_name}</h3>
                        <p className="text-xs text-white/80 mt-1">Rank #{rec.rank}</p>
                      </div>
                      <span className="text-xs font-semibold px-3 py-1 rounded-full bg-white/20">
                        {rec.fit_score}
                      </span>
                    </div>
                  </div>

                  <CardContent className="p-6 space-y-4">
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {rec.description}
                    </p>

                    <div className="space-y-2 text-sm">
                      <div className="flex items-center gap-2 text-foreground font-semibold">
                        <IndianRupee className="w-4 h-4 text-emerald-600" />
                        {rec.estimated_salary || 'Salary info not available'}
                      </div>
                      <div className="flex items-center gap-2 text-xs text-primary font-semibold">
                        <MapPin className="w-4 h-4" />
                        {rec.growth_prospects || 'Growth info not available'}
                      </div>
                    </div>

                    <div className="flex flex-wrap gap-2">
                      {(rec.required_skills || []).map((skill) => (
                        <span
                          key={skill}
                          className="text-xs bg-primary/10 text-primary px-2.5 py-1 rounded-full border border-primary/20"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>

                    <Button
                      className="w-full rounded-xl bg-gradient-to-r from-primary to-violet-600 text-white hover:opacity-90"
                      onClick={() => setSelected(rec)}
                    >
                      View Details
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
        </div>

        {/* Dialog */}
        <Dialog open={!!selected} onOpenChange={() => setSelected(null)}>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto p-0 gap-0 bg-gradient-to-b from-white to-slate-50">
            <div className="bg-gradient-to-br from-primary to-violet-600 p-6 text-white">
              <DialogHeader>
                <DialogTitle className="text-2xl font-bold">
                  {selected?.pathway_name}
                </DialogTitle>
                <p className="text-sm text-white/80 mt-1">Rank #{selected?.rank} • {selected?.fit_score}</p>
              </DialogHeader>
            </div>

            <div className="p-6 space-y-6">
              <section className="space-y-2">
                <div className="flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-primary" />
                  <h3 className="text-lg font-semibold text-foreground">Overview</h3>
                </div>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {selected?.description}
                </p>
              </section>

              {selected?.why_recommended && (
                <section className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Heart className="w-5 h-5 text-rose-600" />
                    <h3 className="text-lg font-semibold text-foreground">Why it’s recommended</h3>
                  </div>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {selected.why_recommended}
                  </p>
                </section>
              )}

              <section className="space-y-3">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                  <h3 className="text-lg font-semibold text-foreground">Required skills</h3>
                </div>
                <div className="flex flex-wrap gap-2">
                  {(selected?.required_skills || []).map((s) => (
                    <span key={s} className="text-xs bg-emerald-50 text-emerald-700 px-2.5 py-1 rounded-full border border-emerald-200">
                      {s}
                    </span>
                  ))}
                </div>
              </section>

              <section className="space-y-2">
                <div className="flex items-center gap-2">
                  <IndianRupee className="w-5 h-5 text-emerald-600" />
                  <h3 className="text-lg font-semibold text-foreground">Salary / Growth</h3>
                </div>
                <p className="text-sm text-muted-foreground">
                  {selected?.estimated_salary || 'Not provided'}
                </p>
                <p className="text-sm text-muted-foreground">
                  {selected?.growth_prospects || 'Growth info not provided'}
                </p>
              </section>

              {(selected?.considerations?.length ?? 0) > 0 && (
                <section className="space-y-2">
                  <div className="flex items-center gap-2">
                    <AlertTriangle className="w-5 h-5 text-amber-600" />
                    <h3 className="text-lg font-semibold text-foreground">Considerations</h3>
                  </div>
                  <ul className="space-y-1 text-sm text-muted-foreground list-disc pl-5">
                    {selected?.considerations.map((c, i) => (
                      <li key={`${c}-${i}`}>{c}</li>
                    ))}
                  </ul>
                </section>
              )}

              {(selected?.next_steps?.length ?? 0) > 0 && (
                <section className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Rocket className="w-5 h-5 text-primary" />
                    <h3 className="text-lg font-semibold text-foreground">Next steps</h3>
                  </div>
                  <div className="space-y-2">
                    {selected?.next_steps.map((step, i) => (
                      <div key={`${step}-${i}`} className="flex items-start gap-3 bg-primary/5 rounded-lg p-3 border border-primary/10">
                        <Calendar className="w-4 h-4 text-primary mt-0.5" />
                        <p className="text-sm text-muted-foreground">{step}</p>
                      </div>
                    ))}
                  </div>
                </section>
              )}

              <section className="space-y-2">
                <div className="flex items-center gap-2">
                  <Info className="w-5 h-5 text-slate-600" />
                  <h3 className="text-lg font-semibold text-foreground">Source & Mode</h3>
                </div>
                <p className="text-xs text-muted-foreground">
                  Source: {apiData.source || 'unknown'} • Demo mode: {apiData.demo_mode ? 'yes' : 'no'}
                </p>
              </section>
            </div>
          </DialogContent>
        </Dialog>

        {/* Footer CTA */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="text-center mt-10"
        >
          <Button 
            variant="outline"
            size="lg" 
            className="rounded-full bg-white hover:bg-white/90 border-border shadow-sm"
            onClick={() => navigate('/get-started')}
          >
            <ArrowLeft className="mr-2 w-4 h-4" />
            Retake Assessment
          </Button>
        </motion.div>
      </main>
    </div>
  );
};

export default Dashboard;