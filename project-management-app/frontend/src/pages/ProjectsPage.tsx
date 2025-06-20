import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const ProjectsPage: React.FC = () => {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Projects</h1>
      <Card>
        <CardHeader>
          <CardTitle>Project Listings</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Project details and management tools will appear here.</p>
        </CardContent>
      </Card>
    </div>
  );
};
export default ProjectsPage;
