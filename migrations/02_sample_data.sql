-- Sample data for Kurasi Map

-- Sample restaurants
INSERT INTO locations (
    name, 
    description, 
    category_id, 
    latitude, 
    longitude, 
    address, 
    operating_hours, 
    instagram, 
    phone, 
    website, 
    typical_spending, 
    images, 
    premium_only
) VALUES
    (
        'Warung Tekko',
        'A cozy Indonesian restaurant with authentic flavors.',
        'restaurants',
        -6.2088,
        106.8456,
        'Jl. Senopati No. 42, Jakarta Selatan',
        '{"Monday": "11:00 - 22:00", "Tuesday": "11:00 - 22:00", "Wednesday": "11:00 - 22:00", "Thursday": "11:00 - 22:00", "Friday": "11:00 - 23:00", "Saturday": "11:00 - 23:00", "Sunday": "11:00 - 22:00"}',
        'warungtekko',
        '+62212751234',
        'https://warungtekko.com',
        'Rp 100,000 - Rp 200,000 per person',
        ARRAY['https://example.com/images/warung-tekko-1.jpg', 'https://example.com/images/warung-tekko-2.jpg'],
        FALSE
    ),
    (
        'Sushi Tei',
        'Japanese restaurant with a wide variety of sushi and sashimi.',
        'restaurants',
        -6.2100,
        106.8470,
        'Pacific Place Mall, Jl. Jend. Sudirman, Jakarta Selatan',
        '{"Monday": "10:00 - 22:00", "Tuesday": "10:00 - 22:00", "Wednesday": "10:00 - 22:00", "Thursday": "10:00 - 22:00", "Friday": "10:00 - 23:00", "Saturday": "10:00 - 23:00", "Sunday": "10:00 - 22:00"}',
        'sushitei_id',
        '+62215701234',
        'https://sushitei.co.id',
        'Rp 150,000 - Rp 300,000 per person',
        ARRAY['https://example.com/images/sushi-tei-1.jpg', 'https://example.com/images/sushi-tei-2.jpg'],
        FALSE
    ),
    (
        'Amuz Gourmet',
        'Fine dining French restaurant with elegant atmosphere.',
        'restaurants',
        -6.2150,
        106.8300,
        'The Energy Building, Jl. Jend. Sudirman Kav. 52-53, Jakarta Selatan',
        '{"Monday": "12:00 - 15:00, 18:00 - 22:00", "Tuesday": "12:00 - 15:00, 18:00 - 22:00", "Wednesday": "12:00 - 15:00, 18:00 - 22:00", "Thursday": "12:00 - 15:00, 18:00 - 22:00", "Friday": "12:00 - 15:00, 18:00 - 23:00", "Saturday": "18:00 - 23:00", "Sunday": "Closed"}',
        'amuzgourmet',
        '+62215201234',
        'https://amuzgourmet.com',
        'Rp 500,000 - Rp 1,500,000 per person',
        ARRAY['https://example.com/images/amuz-1.jpg', 'https://example.com/images/amuz-2.jpg'],
        TRUE
    );

-- Sample cafes
INSERT INTO locations (
    name, 
    description, 
    category_id, 
    latitude, 
    longitude, 
    address, 
    operating_hours, 
    instagram, 
    phone, 
    website, 
    typical_spending, 
    images, 
    premium_only
) VALUES
    (
        'Djournal Coffee',
        'Specialty coffee shop with cozy atmosphere.',
        'cafes',
        -6.2095,
        106.8230,
        'Jl. Wijaya No. 45, Jakarta Selatan',
        '{"Monday": "07:00 - 22:00", "Tuesday": "07:00 - 22:00", "Wednesday": "07:00 - 22:00", "Thursday": "07:00 - 22:00", "Friday": "07:00 - 23:00", "Saturday": "08:00 - 23:00", "Sunday": "08:00 - 22:00"}',
        'djournalcoffee',
        '+62217231234',
        'https://djournalcoffee.com',
        'Rp 50,000 - Rp 100,000 per person',
        ARRAY['https://example.com/images/djournal-1.jpg', 'https://example.com/images/djournal-2.jpg'],
        FALSE
    ),
    (
        'Common Grounds',
        'Modern coffee shop with great ambiance and food menu.',
        'cafes',
        -6.2240,
        106.8300,
        'Citywalk Sudirman, Jl. K.H. Mas Mansyur, Jakarta Pusat',
        '{"Monday": "07:30 - 21:30", "Tuesday": "07:30 - 21:30", "Wednesday": "07:30 - 21:30", "Thursday": "07:30 - 21:30", "Friday": "07:30 - 22:30", "Saturday": "08:30 - 22:30", "Sunday": "08:30 - 21:30"}',
        'commongroundscoffee',
        '+62212551234',
        'https://commongrounds.co.id',
        'Rp 60,000 - Rp 120,000 per person',
        ARRAY['https://example.com/images/common-grounds-1.jpg', 'https://example.com/images/common-grounds-2.jpg'],
        FALSE
    );

-- Sample sports venues
INSERT INTO locations (
    name, 
    description, 
    category_id, 
    latitude, 
    longitude, 
    address, 
    operating_hours, 
    instagram, 
    phone, 
    website, 
    typical_spending, 
    images, 
    premium_only
) VALUES
    (
        'Senayan Golf Club',
        'Premium golf course in the heart of Jakarta.',
        'sports',
        -6.2180,
        106.8020,
        'Jl. Asia Afrika, Senayan, Jakarta Pusat',
        '{"Monday": "06:00 - 19:00", "Tuesday": "06:00 - 19:00", "Wednesday": "06:00 - 19:00", "Thursday": "06:00 - 19:00", "Friday": "06:00 - 19:00", "Saturday": "06:00 - 19:00", "Sunday": "06:00 - 19:00"}',
        'senayangolf',
        '+62215701234',
        'https://senayangolf.com',
        'Rp 500,000 - Rp 1,500,000 per session',
        ARRAY['https://example.com/images/senayan-golf-1.jpg', 'https://example.com/images/senayan-golf-2.jpg'],
        TRUE
    ),
    (
        'Fitness First Platinum',
        'Premium fitness center with state-of-the-art equipment.',
        'sports',
        -6.2260,
        106.8300,
        'Pacific Place Mall, Jl. Jend. Sudirman, Jakarta Selatan',
        '{"Monday": "06:00 - 22:00", "Tuesday": "06:00 - 22:00", "Wednesday": "06:00 - 22:00", "Thursday": "06:00 - 22:00", "Friday": "06:00 - 22:00", "Saturday": "08:00 - 20:00", "Sunday": "08:00 - 20:00"}',
        'fitnessfirstid',
        '+62215701234',
        'https://fitnessfirst.co.id',
        'Rp 300,000 per day pass, Membership from Rp 1,500,000 per month',
        ARRAY['https://example.com/images/fitness-first-1.jpg', 'https://example.com/images/fitness-first-2.jpg'],
        TRUE
    );

-- Sample hospitals
INSERT INTO locations (
    name, 
    description, 
    category_id, 
    latitude, 
    longitude, 
    address, 
    operating_hours, 
    instagram, 
    phone, 
    website, 
    typical_spending, 
    images, 
    premium_only
) VALUES
    (
        'Siloam Hospitals',
        'Modern hospital with comprehensive medical services.',
        'hospitals',
        -6.2200,
        106.8150,
        'Jl. Jend. Sudirman Kav. 50, Jakarta Selatan',
        '{"Monday": "00:00 - 24:00", "Tuesday": "00:00 - 24:00", "Wednesday": "00:00 - 24:00", "Thursday": "00:00 - 24:00", "Friday": "00:00 - 24:00", "Saturday": "00:00 - 24:00", "Sunday": "00:00 - 24:00"}',
        'siloamhospitals',
        '+62215701234',
        'https://siloamhospitals.com',
        'Varies by treatment',
        ARRAY['https://example.com/images/siloam-1.jpg', 'https://example.com/images/siloam-2.jpg'],
        TRUE
    );

-- Sample shopping venues
INSERT INTO locations (
    name, 
    description, 
    category_id, 
    latitude, 
    longitude, 
    address, 
    operating_hours, 
    instagram, 
    phone, 
    website, 
    typical_spending, 
    images, 
    premium_only
) VALUES
    (
        'Plaza Indonesia',
        'Luxury shopping mall with high-end brands.',
        'shopping',
        -6.1930,
        106.8230,
        'Jl. M.H. Thamrin No. 28-30, Jakarta Pusat',
        '{"Monday": "10:00 - 22:00", "Tuesday": "10:00 - 22:00", "Wednesday": "10:00 - 22:00", "Thursday": "10:00 - 22:00", "Friday": "10:00 - 23:00", "Saturday": "10:00 - 23:00", "Sunday": "10:00 - 22:00"}',
        'plazaindonesia',
        '+62213929000',
        'https://plazaindonesia.com',
        'Varies by store',
        ARRAY['https://example.com/images/plaza-indonesia-1.jpg', 'https://example.com/images/plaza-indonesia-2.jpg'],
        TRUE
    ),
    (
        'Grand Indonesia',
        'Large shopping mall with diverse retail options.',
        'shopping',
        -6.1950,
        106.8220,
        'Jl. M.H. Thamrin No. 1, Jakarta Pusat',
        '{"Monday": "10:00 - 22:00", "Tuesday": "10:00 - 22:00", "Wednesday": "10:00 - 22:00", "Thursday": "10:00 - 22:00", "Friday": "10:00 - 23:00", "Saturday": "10:00 - 23:00", "Sunday": "10:00 - 22:00"}',
        'grandindonesia',
        '+62230459999',
        'https://grandindonesia.com',
        'Varies by store',
        ARRAY['https://example.com/images/grand-indonesia-1.jpg', 'https://example.com/images/grand-indonesia-2.jpg'],
        FALSE
    );