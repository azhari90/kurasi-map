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

-- Create policy to allow service role to insert login activities
CREATE POLICY service_role_insert ON public.login_activities 
    FOR INSERT 
    TO authenticated 
    WITH CHECK (true);

-- Create policy to allow admins to view all login activities
CREATE POLICY admin_all_access ON public.login_activities 
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
CREATE POLICY user_own_access ON public.login_activities 
    FOR SELECT 
    TO authenticated 
    USING (user_id::text = auth.uid()::text);

-- Grant permissions
GRANT SELECT, INSERT ON public.login_activities TO authenticated;
GRANT USAGE ON SEQUENCE public.login_activities_id_seq TO authenticated;

-- Add comment
COMMENT ON TABLE public.login_activities IS 'Stores user login activity information'; 