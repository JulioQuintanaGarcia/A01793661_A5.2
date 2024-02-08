# pylint: disable=C0103
# pylint: disable=W0718
"""
Import Libraries for compute sales script
"""
import json
import sys
import time

def compute_sales(price_catalogue, *sales_records_list):
    """
    Function to calculate total cost sales for product price catalogue data.
    """
    try:
        with open(price_catalogue, 'r', encoding='utf-8') as price_file:
            price_data = json.load(price_file)

        with open('SalesResults.txt', 'w', encoding='utf-8') as results_file:
            total_sales = 0
            for sales_record in sales_records_list:
                total_cost = 0
                with open(sales_record, 'r', encoding='utf-8') as sales_file:
                    sales_data = json.load(sales_file)

                    for sale in sales_data:
                        product_name = sale.get('Product')
                        quantity = sale.get('Quantity')
                        if product_name and quantity:
                            matching_products = [product for product in price_data if product.get('title') == product_name]
                            if matching_products:
                                product_price = matching_products[0].get('price')
                                total_cost += quantity * product_price
                            else:
                                print(f"Error: Product {product_name} not found in the price catalogue.")
                        else:
                            print("Error: Invalid item format in sales record.")

                results_file.write(f"{sales_record} total cost = ${total_cost:.2f}\n")
                print(f"{sales_record} total cost = ${total_cost:.2f}")
                total_sales += total_cost

            elapsed_time = time.process_time()
            results_file.write(f"Total sales = ${total_sales:.2f}\n")
            results_file.write(f"Time Elapsed: {elapsed_time} seconds\n")
            print(f"Total sales = ${total_sales:.2f}")
            print(f"Time Elapsed: {elapsed_time} seconds")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}", file=sys.stderr)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
    except KeyError as e:
        print(f"Error accessing key: {e}", file=sys.stderr)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ComputeSales.py <priceCatalogue.json> <salesRecord1.json> <salesRecord2.json> ...")
    else:
        price_catalogue_file = sys.argv[1]
        sales_records = sys.argv[2:]
        compute_sales(price_catalogue_file, *sales_records)