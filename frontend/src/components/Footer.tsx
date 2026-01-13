import { motion } from 'framer-motion';
import { Mail, MapPin, ArrowRight, Send } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import logo from '@/assets/delhi-career-navigator-logo.png';
import footerBg from '@/assets/footer-bg.png';

const Footer = () => {
  const navigate = useNavigate();
  
  const quickLinks = [
    { name: 'Home', href: '#home' },
    { name: 'How It Works', href: '#how-it-works' },
    { name: 'Features', href: '#features' },
    { name: 'Demo', href: '#demo' },
  ];

  return (
    <footer className="relative overflow-hidden">
      {/* CTA Section with Background Image */}
      <section id="demo" className="py-20 md:py-28 relative overflow-hidden">
        {/* Background Image */}
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{ backgroundImage: `url(${footerBg})` }}
        />
        
        {/* Dark overlay for text visibility */}
        <div className="absolute inset-0 bg-gradient-to-b from-slate-900/70 via-slate-900/60 to-slate-900/80" />
        
        {/* Additional overlay for better contrast */}
        <div className="absolute inset-0 bg-primary/30" />
        
        {/* Soft glow accents */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 right-1/4 w-[300px] h-[300px] bg-white/10 rounded-full blur-[100px]" />
          <div className="absolute bottom-1/4 left-1/4 w-[250px] h-[250px] bg-accent/20 rounded-full blur-[80px]" />
        </div>

        <div className="container mx-auto px-4 relative z-10 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="max-w-3xl mx-auto"
          >
            <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-6 leading-tight drop-shadow-lg">
              Ready to Find Your Direction <br className="hidden sm:block" />
              <span className="text-accent drop-shadow-md">After College?</span>
            </h2>
            <p className="text-white/90 text-base md:text-lg max-w-2xl mx-auto mb-10 leading-relaxed drop-shadow-sm">
              Helping Delhi college students explore realistic career paths using AI-guided insights, roadmaps, and local opportunities.
            </p>
            
            <motion.div
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <Button 
                variant="accent" 
                size="lg" 
                className="rounded-full group shadow-lg shadow-accent/30 px-8 py-6 text-base font-semibold"
                onClick={() => navigate('/get-started')}
              >
                Start Your Career Journey
                <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Button>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Main Footer with Background Image */}
      <div className="relative">
        {/* Background Image */}
        <div 
          className="absolute inset-0 bg-cover bg-bottom bg-no-repeat"
          style={{ backgroundImage: `url(${footerBg})` }}
        />
        
        {/* Dark overlay for text visibility */}
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950/95 via-slate-900/90 to-slate-900/85" />
        
        <div className="container mx-auto px-4 py-14 md:py-16 relative z-10">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-10 lg:gap-8">
            {/* Brand Column */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
              className="lg:col-span-4"
            >
              <div className="flex items-center gap-3 mb-5">
                <img 
                  src={logo} 
                  alt="Delhi Career Navigator" 
                  className="h-10 w-auto object-contain"
                />
                <span className="font-display font-bold text-lg text-white drop-shadow-sm">
                  Delhi Career Navigator
                </span>
              </div>
              <p className="text-white/80 text-sm leading-relaxed max-w-sm drop-shadow-sm">
                AI-powered career guidance designed for college students in Delhi — helping them move from confusion to clarity with realistic pathways and actionable roadmaps.
              </p>
            </motion.div>

            {/* Quick Links */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="lg:col-span-2"
            >
              <h3 className="font-semibold text-white text-sm uppercase tracking-wider mb-5 drop-shadow-sm">Quick Links</h3>
              <ul className="space-y-3">
                {quickLinks.map((link) => (
                  <li key={link.name}>
                    <a 
                      href={link.href} 
                      className="text-white/70 hover:text-white transition-colors text-sm drop-shadow-sm"
                    >
                      {link.name}
                    </a>
                  </li>
                ))}
              </ul>
            </motion.div>

            {/* Contact Info */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="lg:col-span-3"
            >
              <h3 className="font-semibold text-white text-sm uppercase tracking-wider mb-5 drop-shadow-sm">Contact</h3>
              <ul className="space-y-3">
                <li>
                  <a 
                    href="mailto:team@delhicareernavigator.in" 
                    className="text-white/70 hover:text-white transition-colors flex items-center gap-2 text-sm drop-shadow-sm"
                  >
                    <Mail className="w-4 h-4 text-accent" />
                    team@delhicareernavigator.in
                  </a>
                </li>
                <li>
                  <div className="text-white/70 flex items-center gap-2 text-sm drop-shadow-sm">
                    <MapPin className="w-4 h-4 text-accent" />
                    New Delhi, India
                  </div>
                </li>
              </ul>
            </motion.div>

            {/* Newsletter */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="lg:col-span-3"
            >
              <h3 className="font-semibold text-white text-sm uppercase tracking-wider mb-5 drop-shadow-sm">Stay Informed</h3>
              <p className="text-white/70 text-sm mb-4 drop-shadow-sm">
                Get updates on career trends, skills, and opportunities relevant to Delhi students.
              </p>
              <div className="flex gap-2">
                <input 
                  type="email" 
                  placeholder="Your email" 
                  className="flex-1 px-4 py-2.5 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg text-white text-sm placeholder:text-white/50 focus:outline-none focus:border-accent/50 focus:ring-1 focus:ring-accent/50 transition-all"
                />
                <Button variant="accent" size="sm" className="rounded-lg px-4">
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </motion.div>
          </div>
        </div>

        {/* Footer Note */}
        <div className="border-t border-white/10 relative z-10">
          <div className="container mx-auto px-4 py-5">
            <p className="text-white/60 text-sm text-center drop-shadow-sm">
              Built for <span className="text-accent font-medium">Delhi AI Grind Hackathon 2026</span>
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
