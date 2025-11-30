# Invoicify - Hotel Invoice System

A comprehensive hotel invoice management system built with Python and Tkinter that generates, manages, and sends professional PDF invoices.

## Features

- **Customer Management**: Store and manage customer information (name, mobile, address, email, Aadhaar)
- **Room Booking**: Track room bookings with check-in/check-out dates and rates
- **Invoice Generation**: Automatically generate professional PDF invoices from Word templates
- **Tax Calculation**: Automatic calculation of CGST and SGST taxes
- **Discount Management**: Apply discounts to invoices
- **Email Integration**: Send invoices directly via email
- **Invoice Viewing**: Open and manage generated invoices
- **Database Support**: SQLite database for storing customer and invoice data

## Technologies Used

- **Python 3.x**
- **Tkinter** - GUI framework
- **SQLite** - Database management
- **docxtpl** - Word template rendering
- **docx2pdf** - Document conversion
- **Pillow** - Image processing
- **tkcalendar** - Date picker widget
- **smtplib** - Email functionality

## Installation

### Prerequisites
- Python 3.x installed on your system

### Required Packages

Install all dependencies:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install python-docx
pip install docxtpl
pip install docx2pdf
pip install tkcalendar
pip install pillow
```

## Project Structure

```
hotel_invoice_system/
├── invoiceSystem.py          # Main application file
├── DBhelper.py               # Database helper functions
├── README.md                 # This file
├── invoiceSW/
│   ├── Template/
│   │   └── INVOICE.docx      # Invoice template
│   └── [Generated invoices]
├── Logo.png                  # Application logo
├── Logo2.png                 # Window icon
└── INvoicifyDataBase.txt     # Database information
```

## Usage

### Running the Application

```bash
python invoiceSystem.py
```

### How to Use

1. **Enter Customer Information**
   - Fill in Name, Mobile Number, Aadhaar Number, City, Address, and Email
   - All fields are validated before submission

2. **Add Room Bookings**
   - Select Check-in and Check-out dates
   - Choose room type (Standard/Deluxe/Suite, AC/Non-AC)
   - Room number and rate are automatically populated
   - Click "Add Item" to add to invoice

3. **Calculate Invoice**
   - Set discount percentage and GST rate
   - Click "Calculate" to compute totals

4. **Generate Invoice**
   - Click "Generate" to create a PDF invoice
   - Invoice is saved in the `invoiceSW/` folder

5. **Send Invoice**
   - Click "Send" to email the invoice to the customer
   - Email validation is performed before sending

6. **Open Invoice**
   - Click "Open" to view the generated PDF
   - Select from file browser or open the current invoice

## File Modes Reference

The application uses various file modes:
- **`'rb'`** - Read binary (used for reading PDF files for email attachment)
- **`'wb'`** - Write binary (used for saving PDF files)
- **`'r+'`** - Read and write text (for database operations)

## Database

The application uses SQLite database with the following main tables:
- **Customers** - Customer information
- **Invoices** - Invoice records
- **Invoice Details** - Individual room bookings per invoice

Database functions are managed through `DBhelper.py`

## Email Configuration

⚠️ **Security Note**: The application currently contains hardcoded email credentials. For production use:
1. Use environment variables for sensitive data
2. Implement OAuth2 authentication
3. Never commit credentials to version control

Current email configuration:
- SMTP Server: smtp.gmail.com
- Port: 465
- App-specific password required for Gmail

## Input Validation

The application validates:
- **Name**: Only letters and spaces
- **Mobile**: Exactly 10 digits
- **Aadhaar**: Exactly 12 digits
- **Email**: Valid email format

## Features in Detail

### Invoice Template
Uses a Word template (`INVOICE.docx`) with the following variables:
- name, mobile, addhar, address, city, email
- invoice_list (room bookings)
- discount, amount, cgst, sgst
- total_amount, total, inno

### Room Types Available
- Standard Non-AC
- Standard AC
- Deluxe Non-AC
- Deluxe AC
- Suite AC

## Future Enhancements

- [ ] Multi-user authentication
- [ ] Payment gateway integration
- [ ] Advanced reporting and analytics
- [ ] Bulk invoice generation
- [ ] Invoice templates customization
- [ ] Cloud backup integration
- [ ] Mobile app version

## Troubleshooting

**Logo not loading?**
- Ensure `Logo.png` and `Logo2.png` are in the same directory as the script

**Template not found?**
- Verify `invoiceSW/Template/INVOICE.docx` exists

**Email sending fails?**
- Check internet connection
- Verify email credentials
- Ensure "Less secure app access" is enabled for Gmail (or use App Password)

**PDF conversion error?**
- Ensure `docx2pdf` is properly installed
- Check file permissions in `invoiceSW/` folder

## License

This project is open source and available under the MIT License.

## Author

Hotel Invoice System Development Team

## Support

For issues, questions, or contributions, please create an issue in the repository.

---

**Last Updated**: November 2025
