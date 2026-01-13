import { motion } from 'framer-motion';
import { Brain, Compass, TrendingUp } from 'lucide-react';
import howItWorksBg from '@/assets/how-it-works-bg.png';

const steps = [
  {
    icon: Brain,
    title: 'AI-Powered Student Profiling',
    description: 'Students share their course, skills, career goals, language preference, financial and time constraints to reflect real-life situations.',
    color: 'from-blue-500 to-indigo-600',
  },
  {
    icon: Compass,
    title: 'Personalized Career Pathways',
    description: 'AI analyzes student data with Delhi-specific education and career insights to suggest primary and backup career paths with clarity.',
    color: 'from-emerald-500 to-teal-600',
  },
  {
    icon: TrendingUp,
    title: 'Roadmaps & Progress Tracking',
    description: 'Students receive step-by-step roadmaps, timelines, skill gap analysis, and curated resources to take action confidently.',
    color: 'from-orange-500 to-amber-600',
  },
];

const HowItWorksSection = () => {
  return (
    <section id="how-it-works" className="py-16 md:py-24 relative overflow-hidden min-h-[600px]">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${howItWorksBg})` }}
      />
      
      {/* Overlay for text readability */}
      <div className="absolute inset-0 bg-gradient-to-b from-white/80 via-white/70 to-white/85" />

      <div className="container mx-auto px-4 relative z-10">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-slate-800 mb-4 drop-shadow-sm">
            How It Works
          </h2>
          <p className="text-slate-700 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
            From confusion to clarity — AI-powered career guidance for Delhi students
          </p>
        </motion.div>

        {/* Steps Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8 max-w-6xl mx-auto">
          {steps.map((step, index) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.15 }}
              className="relative"
            >
              {/* Card */}
              <div className="bg-white/90 backdrop-blur-sm rounded-2xl p-6 md:p-8 shadow-lg shadow-slate-200/50 border border-white/60 h-full hover:shadow-xl hover:bg-white/95 transition-all duration-300 hover:-translate-y-1">
                {/* Step Number & Icon */}
                <div className="flex items-start gap-4 mb-5 md:mb-6">
                  <div className={`relative w-14 h-14 md:w-16 md:h-16 rounded-2xl bg-gradient-to-br ${step.color} flex items-center justify-center shadow-lg flex-shrink-0`}>
                    <step.icon className="w-7 h-7 md:w-8 md:h-8 text-white" />
                    {/* Step Number Badge */}
                    <div className="absolute -top-2 -right-2 w-6 h-6 md:w-7 md:h-7 bg-white rounded-full flex items-center justify-center shadow-md border-2 border-slate-100">
                      <span className="text-xs md:text-sm font-bold text-slate-700">{index + 1}</span>
                    </div>
                  </div>
                </div>

                {/* Content */}
                <h3 className="font-display text-lg md:text-xl font-semibold text-slate-800 mb-2 md:mb-3">
                  {step.title}
                </h3>
                <p className="text-slate-600 leading-relaxed text-sm md:text-base">
                  {step.description}
                </p>
              </div>

              {/* Connector Line (hidden on last item and mobile) */}
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-1/2 -right-4 w-8 h-0.5 bg-gradient-to-r from-slate-400 to-transparent" />
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorksSection;
