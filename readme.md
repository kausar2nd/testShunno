# AlterUSE: A Prototype Recycling Management System

## Project Motivation

*AlterUSE* — a platform designed to promote sustainable recycling practices and bridge the gap between individuals and businesses in managing recyclable materials. The vision is to deploy autonomous collection booths across the city, allowing users to recycle their products conveniently while incentivizing them through a points-based system. Businesses can source recyclable materials through the platform, enabling a circular economy.

Though this is currently a prototype, it demonstrates a viable model for an end-to-end recycling system, covering user submissions, material collection, and distribution.

## Key Features

There are three types of users. 

### *1. General Users:*

- **Submission Requests**: Users can log into the site and create a submission request, receiving a unique code or QR code.
- **Booth Locator**: Users can locate nearby collection booths on a map.
- **Submission History**: View the history of previous submissions.
- **Points Tracking** (Planned): Points earned for submissions can be redeemed for money or vouchers.

### *2. Businesses:*
- **Material Orders**: Companies can order recycled materials directly from the platform.
- **Order History**: View and manage previous orders.

### *3. Admin:*

- **Dashboard Management**: Admins can view registered users, companies, submissions, and orders.
- **Inventory Control**: Edit or delete submission and order records.


## Technical Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL
- **Version Control**: Git & GitHub
- **Hosting**:
  - Fully functional site: Hosted on a subdomain: [AlterUSE](https://alteruse.jobair-hossain.info/ "Visit ALterUSE").
  - UI-only version: Hosted on Vercel: [AlterUSE](https://alteruse.vercel.app "Visit ALterUSE").

## Project Tree Overview

``` bash
AlterUSE
├─ app
│  ├─ routes
│  │  ├─ admin_routes.py     
│  │  ├─ company_routes.py    
│  │  ├─ general_routes.py    
│  │  └─ user_routes.py      
│  ├─ static
│  │  ├─ assets
│  │  ├─ css
│  │  │  ├─ admin_dash_style.css
│  │  │  ├─ company_dashboard_style.css
│  │  │  ├─ find_bin_style.css
│  │  │  ├─ index_styles.css
│  │  │  ├─ login_general_style.css
│  │  │  ├─ login_style.css
│  │  │  └─ user_dashboard_style.css
│  │  └─ js
│  │     ├─ admin_dash_script.js
│  │     ├─ company_dashboard_script.js
│  │     └─ find_bin_script.js
│  ├─ templates
│  │  ├─ admin_dashboard.html
│  │  ├─ admin_login.html
│  │  ├─ company_dashboard.html
│  │  ├─ company_login.html
│  │  ├─ company_signup.html
│  │  ├─ find_bin.html
│  │  ├─ index.html
│  │  ├─ login_general.html
│  │  ├─ user_dashboard.html
│  │  ├─ user_login.html
│  │  └─ user_signup.html
│  ├─ utils
│  │  ├─ auth_utils.py         
│  │  └─ db_utils.py          
│  └─ __init__.py
├─ LICENSE
├─ readme.md
├─ requirements.txt
└─ run.py
```

## Application Workflow

### User Submissions
1. Users log in via their email and password.
2. The submission form allows users to select a branch and input quantities for recyclable materials (plastic bottles, cardboard, glass).
3. Upon submission, the following occurs:
   - The submission is logged in the `user_history` table with details such as email, description, and branch.
   - The corresponding quantities are updated in the `storage` table using SQL queries.
   - Users can view their submission history on the dashboard.

**Key Code Reference:**
- `user_routes.py`: `user_submit()` handles user submissions, inserts data into the database, and updates storage quantities dynamically.

### *Admin Management:*
1. The admin dashboard provides a detailed view of:
   - Registered users and companies.
   - Submission and order logs.
2. Admins can edit or delete submissions/orders:
   - Editing adjusts quantities in the `storage` table while maintaining logs in `user_history` or `company_history`.
   - Deleting removes entries from logs and updates `storage` accordingly.

**Key Code Reference:**
- `admin_routes.py`: `admin_dashboard()` fetches data for users and companies, while routes like `usub_edit` and `usub_delete` manage edits and deletions dynamically.

### *Company Orders:*
1. Companies log in and place orders for recycled materials.
2. Orders are logged in the `company_history` table, and quantities are deducted from `storage`.
3. Companies can view their order history and edit or delete orders.

**Key Code Reference:**
- `company_routes.py`: `company_submit()` Handles order placement and history management.

### *Authentication:*
1. **Login/Signup**:
   - Users, companies, and admins have distinct login routes.
   - All th details are stored in the database.
   - Password validation and session handling ensure secure access.
2. **Access Control**:
   - Decorators like `@login_required` restrict access to authenticated users only.

**Key Code Reference:**
- `auth_utils.py`: Implements `login_required` for session validation.


## Installation & Setup

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/alteruse.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure the database:
   - Create a MySQL database.
   - Update the database credentials in `db_utils.py`.
4. Run the application:
   ```bash
   python run.py
   ```
5. Access the app at `http://127.0.0.1:5000/`.


### Deployment

The application is hosted on a subdomain using cPanel for both the web app and MySQL database. If replicating:

- Use cPanel to deploy the Flask application.
- Migrate your local database to the remote MySQL database in cPanel.


## Current Status & Future Work

### *Completed:*

- User, company, and admin workflows.
- Basic submission and order management.
- Booth locator functionality.

### *Planned:*

- Points system and coupon integration.
- Booth hardware integration for QR/code verification.
- Enhanced admin analytics.
- Blogs and FAQs related to sustainability.


## Live Site

- Fully Functional Site: [AlterUSE](https://alteruse.jobair-hossain.info/)
- UI-Only Version: [Vercel Deployment](https://alteruse.vercel.app)


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code follows the existing style and conventions.

© 2024 Kausar Ahmed