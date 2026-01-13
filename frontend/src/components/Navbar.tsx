import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Menu, X, ArrowRight, Home, Lightbulb, Sparkles, Play } from 'lucide-react';
import { Button } from '@/components/ui/button';
import logo from '@/assets/delhi-career-navigator-logo.png';

const Navbar = () => {
  const navigate = useNavigate();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { name: 'Home', href: '#home', icon: Home },
    { name: 'How It Works', href: '#how-it-works', icon: Lightbulb },
    { name: 'Features', href: '#features', icon: Sparkles },
    { name: 'Demo', href: '#demo', icon: Play },
  ];

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled 
          ? 'bg-white/95 backdrop-blur-xl shadow-lg shadow-primary/10 border-b border-primary/10 py-3' 
          : 'bg-transparent py-4 sm:py-5'
      }`}
    >
      <div className="container mx-auto px-4 flex items-center justify-between">
        {/* Logo */}
        <a href="#" className="flex items-center gap-3 group">
          <motion.div 
            whileHover={{ scale: 1.05 }}
            className="h-11 sm:h-12"
          >
            <img 
              src={logo} 
              alt="Delhi Career Navigator" 
              className="h-full w-auto object-contain"
            />
          </motion.div>
          <div className="flex flex-col leading-none">
            <span className="font-display font-bold text-lg sm:text-xl text-primary-dark tracking-tight">
              Delhi Career
            </span>
            <span className="font-display font-bold text-lg sm:text-xl text-accent tracking-tight">
              Navigator
            </span>
          </div>
        </a>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center gap-10">
          <ul className="flex items-center gap-8">
            {navLinks.map((link, index) => (
              <motion.li 
                key={link.name}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <a
                  href={link.href}
                  className={`font-semibold transition-all duration-200 relative group py-2 ${
                    isScrolled 
                      ? 'text-primary-dark hover:text-primary' 
                      : 'text-primary-dark hover:text-accent'
                  }`}
                >
                  {link.name}
                  <span className="absolute left-0 -bottom-1 w-0 h-0.5 bg-gradient-to-r from-accent to-primary group-hover:w-full transition-all duration-300 rounded-full" />
                </a>
              </motion.li>
            ))}
          </ul>
          <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Button 
              variant="accent" 
              size="lg" 
              className="rounded-full px-7 shadow-lg shadow-accent/30 hover:shadow-xl hover:shadow-accent/40 transition-all duration-300 group"
              onClick={() => navigate('/get-started')}
            >
              Get Started
              <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Button>
          </motion.div>
        </div>

        {/* Mobile Menu Button */}
        <motion.button
          whileTap={{ scale: 0.9 }}
          className="md:hidden p-2.5 rounded-xl bg-primary/5 hover:bg-primary/10 text-primary transition-colors"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        >
          {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </motion.button>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className="md:hidden absolute top-full left-0 right-0 overflow-hidden"
          >
            {/* Gradient background with blur */}
            <div className="relative bg-gradient-to-br from-white via-primary/5 to-accent/10 backdrop-blur-2xl border-t border-primary/10 shadow-2xl shadow-primary/20">
              {/* Decorative elements */}
              <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-accent/20 to-transparent rounded-bl-full" />
              <div className="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-tr from-primary/10 to-transparent rounded-tr-full" />
              
              <div className="container mx-auto px-5 py-6 relative z-10">
                {/* Navigation Links */}
                <ul className="flex flex-col gap-2">
                  {navLinks.map((link, index) => {
                    const IconComponent = link.icon;
                    return (
                      <motion.li 
                        key={link.name}
                        initial={{ opacity: 0, x: -30, scale: 0.9 }}
                        animate={{ opacity: 1, x: 0, scale: 1 }}
                        transition={{ 
                          delay: index * 0.08,
                          type: "spring",
                          stiffness: 300,
                          damping: 24
                        }}
                      >
                        <a
                          href={link.href}
                          className="group flex items-center gap-4 py-4 px-5 rounded-2xl bg-white/60 hover:bg-white border border-primary/5 hover:border-accent/30 shadow-sm hover:shadow-lg hover:shadow-accent/10 transition-all duration-300"
                          onClick={() => setIsMobileMenuOpen(false)}
                        >
                          {/* Icon container with gradient background */}
                          <div className="flex items-center justify-center w-11 h-11 rounded-xl bg-gradient-to-br from-primary/10 to-accent/20 group-hover:from-accent group-hover:to-accent/80 transition-all duration-300 shadow-sm">
                            <IconComponent className="w-5 h-5 text-primary group-hover:text-white transition-colors duration-300" />
                          </div>
                          
                          {/* Text */}
                          <span className="font-semibold text-primary-dark group-hover:text-accent transition-colors duration-300 text-base">
                            {link.name}
                          </span>
                          
                          {/* Arrow indicator */}
                          <ArrowRight className="w-4 h-4 text-muted-foreground/40 group-hover:text-accent ml-auto opacity-0 group-hover:opacity-100 -translate-x-2 group-hover:translate-x-0 transition-all duration-300" />
                        </a>
                      </motion.li>
                    );
                  })}
                </ul>

                {/* Divider with gradient */}
                <div className="my-5 h-px bg-gradient-to-r from-transparent via-primary/20 to-transparent" />

                {/* CTA Button */}
                <motion.div
                  initial={{ opacity: 0, y: 20, scale: 0.9 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  transition={{ delay: 0.35, type: "spring", stiffness: 300, damping: 24 }}
                >
                  <Button 
                    variant="accent" 
                    size="lg" 
                    className="w-full rounded-2xl shadow-xl shadow-accent/40 hover:shadow-2xl hover:shadow-accent/50 group py-6 text-base font-bold transition-all duration-300"
                    onClick={() => {
                      navigate('/get-started');
                      setIsMobileMenuOpen(false);
                    }}
                  >
                    <span className="flex items-center justify-center gap-2">
                      Get Started
                      <ArrowRight className="w-5 h-5 group-hover:translate-x-1.5 transition-transform duration-300" />
                    </span>
                  </Button>
                </motion.div>

                {/* Subtle tagline */}
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.5 }}
                  className="text-center text-xs text-muted-foreground/60 mt-4 font-medium"
                >
                  AI-Powered Career Guidance for Delhi Students
                </motion.p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
};

export default Navbar;
