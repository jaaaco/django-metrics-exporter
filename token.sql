DO $$
BEGIN
    DELETE FROM public.oauth2_provider_refreshtoken
    WHERE access_token_id IN (
        SELECT id
        FROM public.oauth2_provider_accesstoken
        WHERE expires < NOW() - INTERVAL '30 days'
    );

    DELETE FROM public.oauth2_provider_accesstoken
    WHERE expires < NOW() - INTERVAL '30 days';
END $$;
