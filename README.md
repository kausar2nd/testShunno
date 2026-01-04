# ShunnoWaste

A smart recycling management system that connects users, businesses, and collection points through a digital platform. ShunnoWaste streamlines the recycling process with automated inventory management, a points-based rewards system, and real-time tracking capabilities.

## Features

### For Users

- Submit recyclable materials and receive unique codes for booth drop-offs
- Track submission history and earned reward points
- Locate nearby collection booths with interactive map
- View available materials and pricing

### For Businesses

- Browse and purchase available recycled materials
- Place orders and track order history
- Manage company profile and contact information

### For Administrators

- Manage registered users and companies
- Oversee inventory levels and stock management
- Process submissions and orders
- Generate performance reports and analytics

## Technology Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL
- **Deployment:** Vercel
- **Authentication:** Session-based authentication with secure password hashing

## Installation

1. Clone the repository:

```bash
git clone https://github.com/kausar2nd/ShunnoWaste.git
cd ShunnoWaste
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up the database:
   - Import `shunnowaste_db.sql` into your MySQL database
   - Update database credentials in `app/utils/db_utils.py`

4. Run the application:

```bash
python run.py
```

5. Access the application at `http://localhost:5000`

## Deployment

The application is configured for deployment on Vercel. The `vercel.json` configuration file handles routing and build settings.

To deploy:

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow the deployment prompts

## Project Structure

```bash
ShunnoWaste/
├── app/
│   ├── routes/          # API routes
│   ├── static/          
│   ├── templates/       # UI
│   └── utils/         
├── run.py              # entry point
├── requirements.txt
└── vercel.json
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
