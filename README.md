# ISP-system
# Internet Subscription & Billing Management System

## Project Overview
The Internet Subscription & Billing Management System is a web-based application developed using Django.  
It is designed to automate customer subscriptions, billing, and service activation for small and medium Internet Service Providers (ISPs).

The system ensures that internet services are automatically activated upon successful payment and deactivated when subscriptions expire, reducing manual work and billing errors.

---

## Problem Statement
Many small ISPs manage customer subscriptions manually, leading to:
- Late service activation or deactivation
- Billing inconsistencies
- Poor customer experience

This system addresses these challenges by automating subscription management and payment tracking.

---

## Objectives
- Automate internet subscription management
- Track customer payments and subscription expiry dates
- Automatically activate and deactivate services
- Provide dashboards for both administrators and customers
- Improve efficiency and accountability for ISPs

---

## Scope of the System
### Included
- User authentication and role management (Admin and Customer)
- Internet package management
- Subscription creation and renewal
- Simulated payment processing
- Automatic subscription expiry handling
- Admin and customer dashboards

### Excluded
- Real payment gateway integration (e.g., M-Pesa)
- Physical router or network hardware integration
- Mobile application

---

## System Users
1. **Administrator**
   - Create and manage internet packages
   - View all customers and subscriptions
   - Monitor payments and subscription status

2. **Customer**
   - Register and log in
   - Subscribe to internet packages
   - View subscription status and expiry date
   - Make simulated payments

---

## System Features
- Secure user authentication
- Role-based access control
- Automated subscription expiry checks
- Payment history tracking
- Admin reporting dashboard

---

## Technology Stack
- Backend: Django (Python)
- Database: Postgresql
- Frontend: HTML, Tailwind (CDN)
- Task Scheduling: Django-crontab
- Version Control: Git & GitHub

---

## System Architecture
The system follows a modular Django architecture with separate apps for:
- Accounts
- Packages
- Subscriptions
- Payments

---

## Database Design
Key entities in the system include:
- User
- Package
- Subscription
- Payment

Relationships:
- A user can have one active subscription at a time
- A package can have multiple subscriptions
- A subscription can have multiple payments

---

## Automated Subscription Management
A scheduled background task runs daily to:
- Check for expired subscriptions
- Automatically deactivate expired services

This is implemented using `django-crontab`.

---
