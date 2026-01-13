import { motion } from 'framer-motion';
import { Play, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import heroBgDesktop from '@/assets/hero-bg-desktop.png';
import heroBgMobile from '@/assets/hero-bg-mobile.png';

const HeroSection = () => {
  const navigate = useNavigate();
  
  return (
    <section id="home" className="relative min-h-screen overflow-hidden">
      {/* Desktop Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat z-0 hidden md:block"
        style={{ backgroundImage: `url(${heroBgDesktop})` }}
      />
      
      {/* Mobile Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat z-0 md:hidden"
        style={{ backgroundImage: `url(${heroBgMobile})` }}
      />
      
      {/* Subtle overlay for better text readability */}
      <div className="absolute inset-0 bg-gradient-to-b from-white/30 via-transparent to-white/20 z-[1]" />

      <div className="container mx-auto px-4 relative z-10 pt-28 sm:pt-32 md:pt-36 pb-8 md:pb-12">
        <div className="flex flex-col items-center justify-center min-h-[calc(100vh-8rem)] md:min-h-[calc(100vh-10rem)]">
          {/* Content - Positioned at top of hero area */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center max-w-4xl mx-auto mb-auto pt-4 md:pt-8"
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="inline-flex items-center gap-2 bg-primary-dark text-white px-4 py-2 rounded-full text-xs sm:text-sm font-semibold mb-4 shadow-xl"
            >
              <span className="w-2 h-2 bg-accent rounded-full animate-pulse" />
              AI-Powered Career Guidance
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="font-display text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold leading-tight mb-4"
            >
              <span 
                className="text-primary-dark"
                style={{ 
                  textShadow: '2px 2px 0px rgba(255,255,255,1), -1px -1px 0px rgba(255,255,255,1), 0 0 20px rgba(255,255,255,0.9)' 
                }}
              >
                Delhi Career{' '}
              </span>
              <span 
                className="text-accent"
                style={{ 
                  textShadow: '2px 2px 0px rgba(255,255,255,1), -1px -1px 0px rgba(255,255,255,1), 0 0 20px rgba(255,255,255,0.9)' 
                }}
              >
                Navigator
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="text-base sm:text-lg md:text-xl text-primary-dark font-bold mb-3"
              style={{ 
                textShadow: '2px 2px 0px rgba(255,255,255,1), 0 0 15px rgba(255,255,255,0.9)' 
              }}
            >
              AI-Assisted Decision Support for College Students in Delhi
            </motion.p>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="text-primary-dark/90 text-sm sm:text-base mb-10 md:mb-12 max-w-lg mx-auto font-semibold"
              style={{ 
                textShadow: '1px 1px 0px rgba(255,255,255,1), 0 0 10px rgba(255,255,255,0.8)' 
              }}
            >
              Find the right career path with AI-powered guidance just for you.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center items-center mb-16 sm:mb-0"
            >
              <Button 
                variant="accent" 
                size="default" 
                className="rounded-full group shadow-xl hover:shadow-2xl transition-all duration-300 px-5 sm:px-8 py-2 sm:py-3 font-semibold hover:scale-105 text-sm sm:text-base w-auto"
                onClick={() => navigate('/get-started')}
              >
                Get Started
                <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button 
                variant="outline" 
                size="default" 
                className="rounded-full border-2 border-primary-dark bg-white/90 hover:bg-primary-dark hover:text-white transition-all duration-300 px-5 sm:px-8 py-2 sm:py-3 text-primary-dark font-semibold shadow-xl hover:scale-105 text-sm sm:text-base w-auto"
              >
                <Play className="mr-2 w-4 h-4" />
                Watch Demo
              </Button>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
