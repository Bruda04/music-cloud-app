export interface UserModel {
    userId: string;
    email: string;
    role: UserRole;
}

export enum UserRole {
    Admin = 'Admin',
    AuthUser = 'AuthUser',
}
