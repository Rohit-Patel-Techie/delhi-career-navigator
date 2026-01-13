import { z } from 'zod';

// Sanitize string input - removes potential XSS vectors
const sanitizeString = (value: string): string => {
  return value
    .trim()
    // Remove HTML tags
    .replace(/<[^>]*>/g, '')
    // Remove javascript: protocol
    .replace(/javascript:/gi, '')
    // Remove data: protocol (can contain scripts)
    .replace(/data:/gi, '')
    // Remove event handlers
    .replace(/on\w+\s*=/gi, '')
    // Escape special characters that could be used in injection
    .replace(/[<>"'&]/g, (char) => {
      const escapeMap: Record<string, string> = {
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        '&': '&amp;',
      };
      return escapeMap[char] || char;
    });
};

// Custom refined string that sanitizes input
const sanitizedString = z.string().transform(sanitizeString);

// Form data validation schema with strict validation rules
export const formDataSchema = z.object({
  name: sanitizedString
    .pipe(z.string()
      .min(2, { message: 'Name must be at least 2 characters' })
      .max(100, { message: 'Name must be less than 100 characters' })
      .regex(/^[a-zA-Z\s\-'.]+$/, { message: 'Name can only contain letters, spaces, hyphens, apostrophes, and periods' })
    ),
  courseStream: sanitizedString
    .pipe(z.string()
      .min(2, { message: 'Course/Stream must be at least 2 characters' })
      .max(200, { message: 'Course/Stream must be less than 200 characters' })
    ),
  currentSkills: z.enum(['none', 'basic', 'intermediate'], {
    errorMap: () => ({ message: 'Please select a valid skill level' }),
  }),
  careerInclination: z.enum(['tech', 'non-tech', 'undecided'], {
    errorMap: () => ({ message: 'Please select a valid career inclination' }),
  }),
  timeAvailability: z.enum(['low', 'medium', 'high'], {
    errorMap: () => ({ message: 'Please select a valid time availability' }),
  }),
  financialConstraint: z.enum(['yes', 'no'], {
    errorMap: () => ({ message: 'Please select if you have financial constraints' }),
  }),
  preferredLanguage: z.enum(['english', 'hindi'], {
    errorMap: () => ({ message: 'Please select a valid language' }),
  }),
});

export type ValidatedFormData = z.infer<typeof formDataSchema>;

// Validate form data and return sanitized result or errors
export const validateFormData = (data: unknown): { 
  success: boolean; 
  data?: ValidatedFormData; 
  errors?: Record<string, string>;
} => {
  const result = formDataSchema.safeParse(data);
  
  if (result.success) {
    return { success: true, data: result.data };
  }
  
  const errors: Record<string, string> = {};
  result.error.issues.forEach((issue) => {
    const path = issue.path[0] as string;
    errors[path] = issue.message;
  });
  
  return { success: false, errors };
};

// Helper to safely display user data (additional layer of protection)
export const safeDisplayValue = (value: string | undefined): string => {
  if (!value) return '';
  // Decode any escaped entities for display, then re-sanitize
  const decoded = value
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#x27;/g, "'")
    .replace(/&amp;/g, '&');
  return sanitizeString(decoded);
};
