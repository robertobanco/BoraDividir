
import React from 'react';
import type { Transaction } from '../types';
import { ShareIcon } from './icons/ShareIcon';

interface SettlementDisplayProps {
  settlements: Transaction[];
  totalExpenses: number;
  numParticipants: number;
  onOpenSummary: () => void;
}

export const SettlementDisplay: React.FC<SettlementDisplayProps> = ({ settlements, totalExpenses, numParticipants, onOpenSummary }) => {
  const costPerPerson = numParticipants > 0 ? totalExpenses / numParticipants : 0;
  
  return (
    <div className="glass-card rounded-2xl p-6 animate-fade-in">
      <h2 className="text-xl font-bold mb-6 text-slate-900 dark:text-white flex items-center gap-2">
          <span className="bg-violet-100 dark:bg-violet-900/30 text-violet-600 dark:text-violet-300 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold">3</span>
          Resultado da Divisão
      </h2>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
        <div className="bg-gradient-to-br from-slate-50 to-white dark:from-slate-800 dark:to-slate-800/50 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm">
          <p className="text-sm text-slate-500 dark:text-slate-400 mb-1">Total de Despesas</p>
          <p className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
            {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(totalExpenses)}
          </p>
        </div>
        <div className="bg-gradient-to-br from-violet-50 to-white dark:from-violet-900/20 dark:to-slate-800/50 p-4 rounded-xl border border-violet-100 dark:border-violet-900/30 shadow-sm">
           <p className="text-sm text-violet-600 dark:text-violet-300 mb-1">Custo por Pessoa</p>
           <p className="text-2xl font-bold text-violet-700 dark:text-violet-200 tracking-tight">
            {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(costPerPerson)}
          </p>
        </div>
      </div>
      
      <div className="mt-6">
        <h3 className="text-lg font-semibold mb-4 text-slate-800 dark:text-slate-200">Quem paga quem?</h3>
        {settlements.length === 0 ? (
             <div className="flex flex-col items-center justify-center py-8 bg-emerald-50/50 dark:bg-emerald-900/10 rounded-xl border border-emerald-100 dark:border-emerald-900/30">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-emerald-500 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <p className="text-emerald-700 dark:text-emerald-400 font-medium">Tudo certo! Ninguém deve nada.</p>
            </div>
        ) : (
            <div className="grid gap-3">
            {settlements.map((s, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl shadow-sm">
                    <div className="flex items-center gap-3 flex-grow">
                        <div className="flex flex-col">
                            <span className="text-xs text-slate-500 dark:text-slate-400">Devedor</span>
                            <span className="font-semibold text-slate-800 dark:text-slate-200">{s.from}</span>
                        </div>
                        
                        <div className="flex-grow flex justify-center">
                             <div className="flex items-center text-slate-300 dark:text-slate-600">
                                <div className="h-px w-4 sm:w-12 bg-current"></div>
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-slate-400 dark:text-slate-500" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" /></svg>
                             </div>
                        </div>

                        <div className="flex flex-col items-end text-right">
                            <span className="text-xs text-slate-500 dark:text-slate-400">Recebedor</span>
                            <span className="font-semibold text-slate-800 dark:text-slate-200">{s.to}</span>
                        </div>
                    </div>
                    <div className="ml-4 sm:ml-8 pl-4 sm:pl-8 border-l border-slate-100 dark:border-slate-700">
                         <span className="font-bold text-lg text-violet-600 dark:text-violet-400 font-mono">
                            {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(s.amount)}
                        </span>
                    </div>
                </div>
            ))}
            </div>
        )}
      </div>
       <div className="mt-8 flex justify-center">
         <button
            onClick={onOpenSummary}
            className="inline-flex items-center justify-center px-6 py-2 border border-slate-300 dark:border-slate-600 rounded-full text-sm font-medium text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 shadow-sm transition-all"
          >
           <ShareIcon className="h-4 w-4 mr-2 text-slate-500 dark:text-slate-400" />
            Gerar Recibo / Compartilhar
          </button>
      </div>
    </div>
  );
};
