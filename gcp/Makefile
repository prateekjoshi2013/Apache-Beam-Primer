# Makefile for Google Cloud authentication using Cloud Shell

# login using Cloud Shell
login:
	@echo "Authenticating with Google Cloud..."
	@echo "copy the browser window link and open it in window we have logged in to gcp ui and follow instructions"
	gcloud auth application-default login

# Define the target to clean Terraform files and reinitialize
clean:
	@echo "Deleting .terraform directory and Terraform files..."
	# Delete the .terraform directory and suppress error if it doesn't exist
	rm -rf ./main/.terraform
	# Delete the .terraform.lock.hcl file and suppress error if it doesn't exist
	rm -f ./main/.terraform.lock.hcl
	# Delete the .terraform.tfstate file and suppress error if it doesn't exist
	rm -f ./main/terraform.tfstate
	# Delete the .terraform.tfstate.backup file and suppress error if it doesn't exist
	rm -f ./main/terraform.tfstate.backup
	@echo "Cleanup complete."

.PHONY: login clean
