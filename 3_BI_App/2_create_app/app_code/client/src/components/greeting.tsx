import { motion } from 'framer-motion';

export const Greeting = () => {
  return (
    <div
      key="overview"
      className="mx-auto mt-4 flex size-full max-w-3xl flex-col justify-center px-4 md:mt-16 md:px-8"
    >
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 10 }}
        transition={{ delay: 0.3 }}
        className="mb-6 flex items-center gap-3"
      >
        <img 
          src="/entertainment_co_logo.png" 
          alt="Entertainment Co. Logo" 
          className="h-12 w-auto"
        />
        <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text font-bold text-2xl text-transparent md:text-3xl">
          Entertainment Co.
        </span>
      </motion.div>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 10 }}
        transition={{ delay: 0.5 }}
        className="font-semibold text-xl md:text-2xl"
      >
        Welcome to Your Entertainment Hub!
      </motion.div>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 10 }}
        transition={{ delay: 0.6 }}
        className="text-lg text-zinc-500 md:text-xl"
      >
        Ask me anything about tickets, toys, shows, or dive into your data insights.
      </motion.div>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 10 }}
        transition={{ delay: 0.7 }}
        className="mt-4 flex flex-wrap gap-2"
      >
        <span className="rounded-full bg-blue-100 px-3 py-1 text-blue-700 text-sm dark:bg-blue-900/30 dark:text-blue-300">
          Tickets & Events
        </span>
        <span className="rounded-full bg-purple-100 px-3 py-1 text-purple-700 text-sm dark:bg-purple-900/30 dark:text-purple-300">
          Toys & Collectibles
        </span>
        <span className="rounded-full bg-indigo-100 px-3 py-1 text-indigo-700 text-sm dark:bg-indigo-900/30 dark:text-indigo-300">
          Data & Analytics
        </span>
      </motion.div>
    </div>
  );
};
