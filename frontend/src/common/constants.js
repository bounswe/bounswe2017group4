export const AUTH_SERVICE = process.env.NODE_ENV === 'production' ? '' : '';
export const BUSINESS_SERVICE = process.env.NODE_ENV === 'production' ? 'https://api.github.com/' : 'https://api.github.com/';

export const MAIN_DOMAIN = process.env.NODE_ENV === 'production' ? '' : '';
export const HOME_LOGOUT = process.env.NODE_ENV === 'production' ? '' : '';
