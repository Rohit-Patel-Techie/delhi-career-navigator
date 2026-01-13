import { motion } from 'framer-motion';
import { Route, BarChart3, MapPin, ShieldCheck } from 'lucide-react';
import featuresBg from '@/assets/features-bg.png';

const features = [
  {
    icon: Route,
    title: 'AI-Guided, Realistic Career Paths',
    description: 'Get AI-assisted career pathways based on your course, skills, constraints, and goals — focused on realistic options, not overwhelming choices.',
    bgColor: 'bg-blue-500/20',
    iconColor: 'text-blue-300',
    borderColor: 'border-blue-400/30',
  },
  {
    icon: BarChart3,
    title: 'Skill Gap & Readiness Insights',
    description: 'Understand where you stand today, identify skill gaps, and see what is needed to move from your current level to a job-ready stage.',
    bgColor: 'bg-orange-500/20',
    iconColor: 'text-orange-300',
    borderColor: 'border-orange-400/30',
  },
  {
    icon: MapPin,
    title: 'Delhi-Focused Opportunities & Pathways',
    description: "Explore career paths, internships, and learning options relevant to Delhi's colleges, industries, and student ecosystem — not generic global advice.",
    bgColor: 'bg-emerald-500/20',
    iconColor: 'text-emerald-300',
    borderColor: 'border-emerald-400/30',
  },
  {
    icon: ShieldCheck,
    title: 'Responsible AI, Not Blind Decisions',
    description: 'Designed as a guidance and awareness tool — encouraging informed decisions, mentorship, and human judgment rather than replacing them.',
    bgColor: 'bg-purple-500/20',
    iconColor: 'text-purple-300',
    borderColor: 'border-purple-400/30',
  },
];

const FeaturesSection = () => {
  return (
    <section id="features" className="py-16 md:py-24 relative overflow-hidden">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat z-0"
        style={{ backgroundImage: `url(${featuresBg})` }}
      />
      
      {/* Overlay for better text readability */}
      <div className="absolute inset-0 bg-gradient-to-b from-slate-900/60 via-slate-900/50 to-slate-900/70 z-[1]" />

      <div className="container mx-auto px-4 relative z-10">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12 md:mb-16"
        >
          <h2 className="font-display text-2xl sm:text-3xl md:text-4xl font-bold text-white mb-3 drop-shadow-lg">
            Why Delhi Career Navigator?
          </h2>
          <p className="text-white/90 text-sm sm:text-base max-w-2xl mx-auto leading-relaxed drop-shadow-md">
            Built for Delhi college students — practical, inclusive, and future-ready career guidance.
          </p>
        </motion.div>

        {/* Cards Grid - 4 columns desktop, 2 tablet, 1 mobile */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 md:gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              className="group"
            >
              <div className={`bg-white/10 backdrop-blur-md rounded-2xl p-6 h-full shadow-lg hover:shadow-xl transition-all duration-300 border ${feature.borderColor} hover:bg-white/15`}>
                {/* Icon */}
                <div className={`w-12 h-12 rounded-xl ${feature.bgColor} backdrop-blur-sm flex items-center justify-center mb-5 border ${feature.borderColor}`}>
                  <feature.icon className={`w-6 h-6 ${feature.iconColor}`} />
                </div>

                {/* Content */}
                <h3 className="font-display text-base sm:text-lg font-semibold text-white mb-2 leading-snug">
                  {feature.title}
                </h3>
                <p className="text-white/80 text-sm leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
