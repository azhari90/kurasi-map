-- Create login_activities table
CREATE TABLE IF NOT EXISTS public.login_activities (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    email TEXT NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    device_info TEXT,
    login_status TEXT NOT NULL,
    login_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    location TEXT
);

-- Add indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_login_activities_user_id ON public.login_activities(user_id);
CREATE INDEX IF NOT EXISTS idx_login_activities_login_time ON public.login_activities(login_time);
CREATE INDEX IF NOT EXISTS idx_login_activities_login_status ON public.login_activities(login_status);

-- Add RLS (Row Level Security) policies
ALTER TABLE public.login_activities ENABLE ROW LEVEL SECURITY;

-- Temporarily disable RLS for development
ALTER TABLE public.login_activities DISABLE ROW LEVEL SECURITY;

-- Grant permissions
GRANT SELECT, INSERT ON public.login_activities TO authenticated;
GRANT USAGE ON SEQUENCE public.login_activities_id_seq TO authenticated;
GRANT SELECT, INSERT ON public.login_activities TO anon;
GRANT USAGE ON SEQUENCE public.login_activities_id_seq TO anon;

-- Add comment
COMMENT ON TABLE public.login_activities IS 'Stores user login activity information';

-- NOTE: In production, you should re-enable RLS and set up proper policies:
/*
-- Re-enable RLS
ALTER TABLE public.login_activities ENABLE ROW LEVEL SECURITY;

-- Create policy to allow inserting login activities
CREATE POLICY insert_login_activities ON public.login_activities 
    FOR INSERT 
    TO authenticated, anon
    WITH CHECK (true);

-- Create policy to allow admins to view all login activities
CREATE POLICY admin_select_login_activities ON public.login_activities 
    FOR SELECT 
    TO authenticated 
    USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.users.id = auth.uid()
            AND auth.users.role = 'admin'
        )
    );

-- Create policy to allow users to view only their own login activities
CREATE POLICY user_select_login_activities ON public.login_activities 
    FOR SELECT 
    TO authenticated 
    USING (user_id::text = auth.uid()::text);
*/ 