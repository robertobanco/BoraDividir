
import React, { useState, useRef } from 'react';
import type { Participant } from '../types';
import { UserPlusIcon } from './icons/UserPlusIcon';
import { TrashIcon } from './icons/TrashIcon';
import { PencilIcon } from './icons/PencilIcon';
import { ChevronDownIcon } from './icons/ChevronDownIcon';

interface ParticipantManagerProps {
  participants: Participant[];
  onAddParticipant: (name: string) => void;
  onRemoveParticipant: (id: string) => void;
  onUpdateParticipant: (id: string, name: string) => void;
  isExpanded: boolean;
  onToggle: () => void;
}

const getInitials = (name: string) => {
    return name
        .split(' ')
        .map(word => word[0])
        .slice(0, 2)
        .join('')
        .toUpperCase();
};

const getAvatarColor = (name: string) => {
    const colors = [
        'from-red-400 to-orange-400',
        'from-amber-400 to-yellow-400',
        'from-lime-400 to-green-400',
        'from-emerald-400 to-teal-400',
        'from-cyan-400 to-sky-400',
        'from-blue-400 to-indigo-400',
        'from-violet-400 to-purple-400',
        'from-fuchsia-400 to-pink-400',
        'from-rose-400 to-red-400'
    ];
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    return colors[Math.abs(hash) % colors.length];
};

export const ParticipantManager: React.FC<ParticipantManagerProps> = ({ participants, onAddParticipant, onRemoveParticipant, onUpdateParticipant, isExpanded, onToggle }) => {
  const [name, setName] = useState('');
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editingName, setEditingName] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim()) {
      onAddParticipant(name);
      setName('');
      setTimeout(() => {
        inputRef.current?.focus();
      }, 0);
    }
  };

  const handleStartEdit = (participant: Participant) => {
    setEditingId(participant.id);
    setEditingName(participant.name);
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditingName('');
  };

  const handleSaveEdit = (id: string) => {
    if(editingName.trim()) {
      onUpdateParticipant(id, editingName);
      handleCancelEdit();
    }
  };

  return (
    <div className="glass-card rounded-2xl transition-all duration-300 overflow-hidden">
      <div 
        onClick={onToggle} 
        className="p-5 sm:p-6 flex items-center justify-between cursor-pointer hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors select-none"
      >
        <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
                <span className="bg-violet-100 dark:bg-violet-900/30 text-violet-600 dark:text-violet-300 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">1</span>
                <h2 className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white">
                    Participantes
                </h2>
            </div>
        </div>

        <div className="flex items-center gap-3">
             {!isExpanded && participants.length > 0 && (
                 <div className="flex items-center animate-fade-in">
                    {/* Mobile View Summary */}
                    <div className="sm:hidden">
                        <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
                           {participants.length} pess.
                        </span>
                    </div>

                    {/* Desktop View Summary */}
                    <div className="hidden sm:flex items-center -space-x-2 overflow-hidden mr-2">
                        {participants.slice(0, 5).map((p) => (
                            <div key={p.id} className={`w-6 h-6 rounded-full bg-gradient-to-br ${getAvatarColor(p.name)} ring-2 ring-white dark:ring-slate-800`}></div>
                        ))}
                        {participants.length > 5 && (
                            <div className="w-6 h-6 rounded-full bg-slate-200 dark:bg-slate-700 ring-2 ring-white dark:ring-slate-800 flex items-center justify-center text-[9px] font-bold text-slate-600">+{participants.length - 5}</div>
                        )}
                         <span className="ml-3 text-sm text-slate-500 dark:text-slate-400">{participants.length} pessoa{participants.length !== 1 ? 's' : ''}</span>
                     </div>
                 </div>
            )}
            <ChevronDownIcon className={`h-5 w-5 text-slate-400 transition-transform duration-300 flex-shrink-0 ${isExpanded ? 'rotate-180' : ''}`} />
        </div>
      </div>
      
      {isExpanded && (
      <div className="px-4 pb-6 sm:px-6 animate-fade-in">
        <form onSubmit={handleSubmit} className="relative mb-6 group">
            <input
            ref={inputRef}
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Adicionar pessoa..."
            className="w-full pl-4 pr-14 py-3 bg-slate-100 dark:bg-slate-800/50 border-none rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-violet-500 transition-all"
            />
            <button
            type="submit"
            disabled={!name.trim()}
            className="absolute right-2 top-2 bottom-2 bg-white dark:bg-slate-700 text-violet-600 dark:text-violet-400 p-2 rounded-lg shadow-sm hover:bg-violet-50 dark:hover:bg-slate-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
            <UserPlusIcon className="h-5 w-5"/>
            </button>
        </form>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
            {participants.map((p) => (
                <div key={p.id} className="group relative flex items-center gap-3 p-3 bg-white dark:bg-slate-800/40 border border-slate-100 dark:border-slate-700 rounded-xl shadow-sm hover:shadow-md transition-all hover:border-violet-200 dark:hover:border-violet-900/50">
                    {editingId === p.id ? (
                        <div className="flex-grow flex items-center gap-2">
                        <input
                            type="text"
                            value={editingName}
                            onChange={(e) => setEditingName(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSaveEdit(p.id)}
                            className="w-full px-2 py-1 bg-white dark:bg-slate-900 border border-violet-500 rounded-md text-sm"
                            autoFocus
                            />
                            <button onClick={() => handleSaveEdit(p.id)} className="text-xs font-bold text-violet-600 dark:text-violet-400">OK</button>
                        </div>
                    ) : (
                        <>
                            <div className={`w-10 h-10 rounded-full bg-gradient-to-br ${getAvatarColor(p.name)} flex items-center justify-center text-white font-bold text-sm shadow-sm flex-shrink-0`}>
                                {getInitials(p.name)}
                            </div>
                            <span className="font-medium text-slate-700 dark:text-slate-200 truncate flex-grow">{p.name}</span>
                            
                            <div className="flex opacity-100 sm:opacity-0 group-hover:opacity-100 transition-opacity absolute right-2 bg-white/90 dark:bg-slate-800/90 backdrop-blur p-1 rounded-lg shadow-sm">
                                <button 
                                    onClick={() => handleStartEdit(p)}
                                    className="p-1.5 text-slate-400 hover:text-blue-500 transition-colors"
                                >
                                    <PencilIcon className="h-4 w-4" />
                                </button>
                                <button 
                                    onClick={() => onRemoveParticipant(p.id)}
                                    className="p-1.5 text-slate-400 hover:text-red-500 transition-colors"
                                >
                                    <TrashIcon className="h-4 w-4" />
                                </button>
                            </div>
                        </>
                    )}
                </div>
            ))}
            
            {participants.length === 0 && (
                <div className="col-span-full text-center py-6 border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl text-slate-400">
                    <p className="text-sm">Nenhum participante ainda.</p>
                </div>
            )}
        </div>
        
        {participants.length > 0 && (
            <div className="mt-6 flex justify-center">
                 <button onClick={onToggle} className="text-xs text-slate-400 hover:text-violet-500 flex items-center gap-1 transition-colors">
                    Recolher seção <ChevronDownIcon className="h-3 w-3 rotate-180" />
                 </button>
            </div>
        )}
      </div>
      )}
    </div>
  );
};
