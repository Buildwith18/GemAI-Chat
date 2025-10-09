import React from 'react';
import { DivideIcon as LucideIcon } from 'lucide-react';

interface StatsCardProps {
  label: string;
  value: number;
  icon: LucideIcon;
}

export default function StatsCard({ label, value, icon: Icon }: StatsCardProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm font-medium">{label}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
        </div>
        <div className="p-3 bg-gradient-to-r from-blue-600 to-indigo-700 rounded-xl">
          <Icon className="h-6 w-6 text-white" />
        </div>
      </div>
    </div>
  );
}