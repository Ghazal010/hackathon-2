import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// This function checks authentication for protected routes
export function middleware(request: NextRequest) {
  // Define protected routes
  const protectedPaths = ['/dashboard'];
  const isProtectedPath = protectedPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  );

  // If accessing a protected route
  if (isProtectedPath) {
    // Check if user has a valid token
    const token = request.cookies.get('access_token')?.value ||
                  request.headers.get('authorization')?.replace('Bearer ', '');

    // If no token, redirect to login
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url));
    }

    // In a real implementation, you would verify the token here
    // For now, we'll just allow access if a token exists
  }

  return NextResponse.next();
}

// Specify which paths the middleware should run for
export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*'],
};