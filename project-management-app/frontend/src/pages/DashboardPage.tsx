import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const DashboardPage: React.FC = () => {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Dashboard Overview</h1>
      <Card>
        <CardHeader>
          <CardTitle>Welcome!</CardTitle>
        </CardHeader>
        <CardContent>
          <p>This is your main dashboard. More widgets and information will be added here soon.</p>
          <p className="mt-2">Navigate using the sidebar.</p>
        </CardContent>
      </Card>
      {/* Add more placeholder cards or content */}
    </div>
  );
};
export default DashboardPage;
