import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  ArrowRight, 
  GraduationCap, 
  Briefcase, 
  Clock, 
  Wallet, 
  Languages, 
  CheckCircle2, 
  Compass, 
  User,
  Sparkles,
  Shield
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { toast } from 'sonner';
import { validateFormData, type ValidatedFormData } from '@/lib/formValidation';
import logo from '@/assets/delhi-career-navigator-logo.png';
import getStartedBg from '@/assets/get-started-bg.jpg';

interface FormData {
  name: string;
  courseStream: string;
  currentSkills: string;
  careerInclination: string;
  timeAvailability: string;
  financialConstraint: string; // 'yes' | 'no'
  preferredLanguage: string;   // 'english' | 'hindi'
}

interface FormErrors {
  name?: string;
  courseStream?: string;
  currentSkills?: string;
  careerInclination?: string;
  timeAvailability?: string;
  financialConstraint?: string;
  preferredLanguage?: string;
}

const API_URL = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000/api/recommend/';
const LS_FORM_KEY = 'dcn_formData';
const LS_REC_KEY = 'dcn_recommendations';

const GetStarted = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState<FormData>({
    name: '',
    courseStream: '',
    currentSkills: '',
    careerInclination: '',
    timeAvailability: '',
    financialConstraint: '',
    preferredLanguage: '',
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  // Hydrate form from localStorage
  useEffect(() => {
    try {
      const stored = localStorage.getItem(LS_FORM_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as Partial<FormData>;
        setFormData((prev) => ({ ...prev, ...parsed }));
      }
    } catch (err) {
      console.warn('Unable to parse stored form data', err);
    }
    window.scrollTo(0, 0);
  }, []);

  const handleInputChange = (field: keyof FormData, value: string) => {
    const maxLengths: Partial<Record<keyof FormData, number>> = {
      name: 100,
      courseStream: 200,
    };
    const maxLength = maxLengths[field];
    const truncatedValue = maxLength ? value.slice(0, maxLength) : value;

    setFormData((prev) => ({ ...prev, [field]: truncatedValue }));
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const validationResult = validateFormData(formData);
    if (!validationResult.success) {
      const newErrors: FormErrors = {};
      if (validationResult.errors) {
        Object.entries(validationResult.errors).forEach(([key, message]) => {
          newErrors[key as keyof FormErrors] = message;
        });
      }
      setErrors(newErrors);
      toast.error('Please fill in all required fields correctly');
      return;
    }

    setIsSubmitting(true);

    const payload = {
      name: formData.name,
      course_stream: formData.courseStream,
      covered_skills: formData.currentSkills,
      career_inclination: formData.careerInclination,
      time_availability: formData.timeAvailability,
      financial_constraint: formData.financialConstraint === 'yes',
      preferred_language: formData.preferredLanguage,
    };

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const json = await response.json();

      if (!response.ok) {
        const msg =
          json?.error ||
          json?.details ||
          'Something went wrong while generating recommendations.';
        toast.error(msg);
        return;
      }

      // Persist to localStorage
      localStorage.setItem(LS_FORM_KEY, JSON.stringify(formData));
      localStorage.setItem(LS_REC_KEY, JSON.stringify(json));

      toast.success('Recommendations generated! Redirecting...');
      setIsSubmitted(true);

      const sanitizedData: ValidatedFormData = validationResult.data!;
      navigate('/dashboard', { state: { formData: sanitizedData, recommendations: json } });
    } catch (err) {
      console.error(err);
      toast.error('Unable to reach the server. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const formFields = [
    {
      id: 'name',
      label: 'Name',
      icon: User,
      type: 'input',
      placeholder: 'e.g., Rahul Sharma',
      helperText: null,
    },
    {
      id: 'courseStream',
      label: 'Course / Stream',
      icon: GraduationCap,
      type: 'input',
      placeholder: 'e.g., B.Tech, BA, B.Com, BBA...',
      helperText: null,
    },
    {
      id: 'currentSkills',
      label: 'Current Skills Level',
      icon: Briefcase,
      type: 'radio',
      helperText: 'This helps us adjust learning timelines and expectations.',
      options: [
        { value: 'none', label: 'None', description: 'Just starting out' },
        { value: 'basic', label: 'Basic', description: 'Fundamental knowledge' },
        { value: 'intermediate', label: 'Intermediate', description: 'Hands-on experience' },
      ],
    },
    {
      id: 'careerInclination',
      label: 'Career Inclination',
      icon: Compass,
      type: 'radio',
      helperText: null,
      options: [
        { value: 'tech', label: 'Tech', description: 'Software, Data, AI' },
        { value: 'non-tech', label: 'Non-Tech', description: 'Management, Arts, Law, etc.' },
        { value: 'undecided', label: 'Undecided', description: 'Want to explore options' },
      ],
    },
    {
      id: 'timeAvailability',
      label: 'Time Availability',
      icon: Clock,
      type: 'radio',
      helperText: null,
      options: [
        { value: 'low', label: 'Low', description: '<5 hrs/week' },
        { value: 'medium', label: 'Medium', description: '5–15 hrs/week' },
        { value: 'high', label: 'High', description: '15+ hrs/week' },
      ],
    },
    {
      id: 'financialConstraint',
      label: 'Financial Constraint',
      icon: Wallet,
      type: 'radio',
      helperText: null,
      options: [
        { value: 'yes', label: 'Yes', description: 'Need budget-friendly options' },
        { value: 'no', label: 'No', description: 'Flexible budget' },
      ],
    },
    {
      id: 'preferredLanguage',
      label: 'Preferred Language',
      icon: Languages,
      type: 'radio',
      helperText: null,
      options: [
        { value: 'english', label: 'English', description: '' },
        { value: 'hindi', label: 'Hindi', description: '' },
      ],
    },
  ];

  if (isSubmitted) {
    return (
      <div className="min-h-screen relative flex items-center justify-center p-4 overflow-hidden">
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{ backgroundImage: `url(${getStartedBg})` }}
        />
        <div className="absolute inset-0 bg-gradient-to-b from-sky-100/80 via-sky-50/70 to-white/90" />
        
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-card/95 backdrop-blur-sm rounded-3xl shadow-card p-8 md:p-12 max-w-lg text-center relative z-10"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
            className="w-20 h-20 bg-green-100 rounded-full flex itemsCenter justifyCenter mx-auto mb-6"
          >
            <CheckCircle2 className="w-10 h-10 text-green-600" />
          </motion.div>
          <h2 className="font-display text-2xl md:text-3xl font-bold text-primary-dark mb-4">
            Profile Submitted!
          </h2>
          <p className="text-muted-foreground mb-8">
            Thank you for sharing your details. Our AI is analyzing your profile to create personalized career recommendations for you.
          </p>
          <Button 
            variant="accent" 
            size="xl" 
            className="rounded-full"
            onClick={() => navigate('/')}
          >
            Back to Home
            <ArrowRight className="ml-2 w-5 h-5" />
          </Button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen relative overflow-hidden">
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${getStartedBg})` }}
      />
      <div className="absolute inset-0 bg-gradient-to-b from-background/90 via-background/85 to-background/95" />
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-10 right-10 w-[400px] h-[400px] bg-primary/5 rounded-full blur-[120px]" />
        <div className="absolute bottom-20 left-10 w-[350px] h-[350px] bg-accent/5 rounded-full blur-[100px]" />
        <div className="absolute top-1/4 left-5 w-2 h-32 bg-accent/10 rounded-full" />
        <div className="absolute top-1/3 right-8 w-2 h-24 bg-primary/10 rounded-full" />
      </div>

      <div className="container mx-auto px-4 py-6 relative z-10">
        <motion.button
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          onClick={() => navigate('/')}
          className="flex items-center gap-2 text-muted-foreground hover:text-primary transition-colors group"
        >
          <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
          <span className="font-medium">Back to Home</span>
        </motion.button>
      </div>

      <div className="container mx-auto px-4 pb-16 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-2xl mx-auto"
        >
          <div className="text-center mb-8">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
              className="mx-auto mb-5"
            >
              <img 
                src={logo} 
                alt="Delhi Career Navigator" 
                className="h-16 w-auto object-contain mx-auto"
              />
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="flex items-center justify-center gap-2 mb-3"
            >
              <Sparkles className="w-5 h-5 text-accent" />
              <span className="text-sm font-medium text-accent uppercase tracking-wide">AI-Powered Guidance</span>
            </motion.div>
            
            <h1 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-4">
              Let's Get Started
            </h1>
            <p className="text-muted-foreground text-base md:text-lg max-w-lg mx-auto leading-relaxed">
              Your answers help us suggest realistic career paths based on your background, time, and constraints.
            </p>
          </div>

          <motion.form
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            onSubmit={handleSubmit}
            className="bg-card rounded-2xl shadow-xl border border-border/50 p-6 md:p-8 space-y-6"
          >
            {formFields.map((field, index) => (
              <motion.div
                key={field.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
                className="space-y-3"
              >
                <div className="space-y-1">
                  <Label className="flex items-center gap-2 text-sm font-semibold text-foreground">
                    <span className="flex items-center justify-center w-8 h-8 rounded-lg bg-primary/10">
                      <field.icon className="w-4 h-4 text-primary" />
                    </span>
                    {field.label}
                    <span className="text-destructive">*</span>
                  </Label>
                  {field.helperText && (
                    <p className="text-xs text-muted-foreground ml-10">{field.helperText}</p>
                  )}
                </div>

                {field.type === 'input' ? (
                  <div className="ml-10">
                    <Input
                      value={formData[field.id as keyof FormData]}
                      onChange={(e) => handleInputChange(field.id as keyof FormData, e.target.value)}
                      placeholder={field.placeholder}
                      className={`h-11 rounded-lg border transition-all bg-background focus:ring-2 focus:ring-primary/20 ${
                        errors[field.id as keyof FormErrors] 
                          ? 'border-destructive focus:border-destructive' 
                          : 'border-input focus:border-primary'
                      }`}
                    />
                    {errors[field.id as keyof FormErrors] && (
                      <p className="text-destructive text-xs mt-1.5 flex items-center gap-1">
                        <span className="w-1 h-1 rounded-full bg-destructive" />
                        {errors[field.id as keyof FormErrors]}
                      </p>
                    )}
                  </div>
                ) : (
                  <div className="ml-10">
                    <RadioGroup
                      value={formData[field.id as keyof FormData]}
                      onValueChange={(value) => handleInputChange(field.id as keyof FormData, value)}
                      className={`grid gap-2.5 ${
                        field.options && field.options.length === 2 
                          ? 'grid-cols-2' 
                          : 'grid-cols-1 sm:grid-cols-3'
                      }`}
                    >
                      {field.options?.map((option) => (
                        <Label
                          key={option.value}
                          htmlFor={`${field.id}-${option.value}`}
                          className={`
                            relative flex flex-col items-center justify-center p-3.5 rounded-xl border-2 cursor-pointer transition-all duration-200
                            ${formData[field.id as keyof FormData] === option.value
                              ? 'border-primary bg-primary/5 shadow-sm ring-2 ring-primary/10'
                              : 'border-border bg-background hover:border-primary/40 hover:bg-muted/30'
                            }
                            ${errors[field.id as keyof FormErrors] ? 'border-destructive/30' : ''}
                          `}
                        >
                          <RadioGroupItem
                            value={option.value}
                            id={`${field.id}-${option.value}`}
                            className="sr-only"
                          />
                          {formData[field.id as keyof FormData] === option.value && (
                            <motion.div
                              initial={{ scale: 0 }}
                              animate={{ scale: 1 }}
                              className="absolute -top-1.5 -right-1.5 w-5 h-5 bg-primary rounded-full flex items-center justify-center"
                            >
                              <CheckCircle2 className="w-3.5 h-3.5 text-primary-foreground" />
                            </motion.div>
                          )}
                          <span className="font-semibold text-sm text-foreground">{option.label}</span>
                          {option.description && (
                            <span className="text-xs text-muted-foreground mt-0.5 text-center leading-tight">
                              {option.description}
                            </span>
                          )}
                        </Label>
                      ))}
                    </RadioGroup>
                    {errors[field.id as keyof FormErrors] && (
                      <p className="text-destructive text-xs mt-1.5 flex items-center gap-1">
                        <span className="w-1 h-1 rounded-full bg-destructive" />
                        {errors[field.id as keyof FormErrors]}
                      </p>
                    )}
                  </div>
                )}
              </motion.div>
            ))}

            <div className="pt-4">
              <div className="h-px bg-border" />
            </div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="pt-2"
            >
              <Button
                type="submit"
                variant="accent"
                size="xl"
                className="w-full rounded-xl group font-semibold text-base h-14"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <span className="flex items-center gap-2">
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                      className="w-5 h-5 border-2 border-accent-foreground/30 border-t-accent-foreground rounded-full"
                    />
                    Analyzing your profile...
                  </span>
                ) : (
                  <>
                    Get My Career Recommendations
                    <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </Button>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.7 }}
              className="flex items-start gap-2 p-3 rounded-lg bg-muted/50 border border-border/50"
            >
              <Shield className="w-4 h-4 text-muted-foreground mt-0.5 flex-shrink-0" />
              <p className="text-xs text-muted-foreground leading-relaxed">
                <span className="font-medium">Responsible AI Notice:</span> This tool provides guidance and awareness, not final decisions. Students are encouraged to consult mentors and advisors.
              </p>
            </motion.div>
          </motion.form>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="text-center mt-6 flex items-center justify-center gap-2 text-muted-foreground"
          >
            <div className="w-1.5 h-1.5 rounded-full bg-green-500" />
            <p className="text-xs">
              No login required • Your data stays private
            </p>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default GetStarted;