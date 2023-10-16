# Copyright (c) 2023, Akshat Gupta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
from frappe.utils import formatdate

class RecurringTask(Document):
	def validate(self):
        # Convert start and end dates to datetime objects
		actual_start_date = datetime.strptime(self.actual_start_date, '%Y-%m-%d')
		actual_end_date = datetime.strptime(self.actual_end_date, '%Y-%m-%d')

		# Check if start date is greater than end date
		if actual_start_date > actual_end_date:
			frappe.throw("Actual Start Date must be less than or equal to Actual End Date")

	def on_submit(self):
        # Check frequency and call the appropriate method
		if self.frequency != "Daily":
			self.create_task_for_custom_days()
		else:
			self.create_task_from_recurring()

	def create_task_from_recurring(self):
		# Get start and end dates
		start_date = datetime.strptime(self.actual_start_date, '%Y-%m-%d').date()
		end_date = datetime.strptime(self.actual_end_date, '%Y-%m-%d').date()

		# Check if both start and end dates are set
		if not (start_date and end_date):
			frappe.msgprint("Please set both Actual Start Date and Actual End Date.")
			return

		# Convert for_which_day to integer
		for_which_day = int(self.for_which_day)

		current_date = start_date
		while current_date <= end_date:
			# Create a new Task document
			task = frappe.new_doc("Task")
			# Set the subject and project for the task
			task.subject = f"{self.subject} for {formatdate(current_date, 'dd MMMM')}"
			task.project = self.project

			# Calculate the exp_start_date and exp_end_date
			exp_start_date = current_date - timedelta(days=for_which_day)
			exp_end_date = current_date - timedelta(days=for_which_day)

			task.exp_start_date = exp_start_date.strftime('%Y-%m-%d')
			task.exp_end_date = exp_end_date.strftime('%Y-%m-%d')

			# Save the task document
			task.save()

			# Move to the next date
			current_date += timedelta(days=1)

		frappe.msgprint(f"Created tasks for {self.name}")

	def create_task_for_custom_days(self):
		# Get start and end dates
		start_date = datetime.strptime(self.actual_start_date, '%Y-%m-%d').date()
		end_date = datetime.strptime(self.actual_end_date, '%Y-%m-%d').date()

		# Check if both start and end dates are set
		if not (start_date and end_date):
			frappe.msgprint("Please set both Actual Start Date and Actual End Date.")
			return

		# Get the selected days from the repeat_on_days property
		selected_days = [day.day for day in self.repeat_on_days]
		# Convert for_which_day to integer
		for_which_day = int(self.for_which_day)

		current_date = start_date
		while current_date <= end_date:
			# Check if the current day is in the list of selected days
			if current_date.strftime('%A') in selected_days:
				# Create a new Task document
				task = frappe.new_doc("Task")
				# Set the subject and project for the task
				task.subject = f"{self.subject} for {formatdate(current_date, 'dd MMMM')}"
				task.project = self.project

				# Calculate the exp_start_date and exp_end_date
				exp_start_date = current_date - timedelta(days=for_which_day)
				exp_end_date = current_date - timedelta(days=for_which_day)

				task.exp_start_date = exp_start_date.strftime('%Y-%m-%d')
				task.exp_end_date = exp_end_date.strftime('%Y-%m-%d')

				# Save the task document
				task.save()

			current_date += timedelta(days=1)

		frappe.msgprint(f"Created tasks for {self.name}")

	def update_tasks_from_recurring(self):
		# Get start and end dates
		start_date = datetime.strptime(self.actual_start_date, '%Y-%m-%d').date()
		end_date = datetime.strptime(self.actual_end_date, '%Y-%m-%d').date()

		# Check if both start and end dates are set
		if not (start_date and end_date):
			frappe.msgprint("Please set both Actual Start Date and Actual End Date.")
			return

		# Convert for_which_day to integer
		for_which_day = int(self.for_which_day)

		current_date = start_date
		while current_date <= end_date:
			# Check if task already exists for this date
			existing_task = frappe.get_all("Task", filters={"subject": f"{self.subject} for {formatdate(current_date, 'dd MMMM')}"})
			if existing_task:
				task = frappe.get_doc("Task", existing_task[0].name)
			else:
				task = frappe.new_doc("Task")

			# Set the subject and project for the task
			task.subject = f"{self.subject} for {formatdate(current_date, 'dd MMMM')}"
			task.project = self.project

			# Calculate the exp_start_date and exp_end_date
			exp_start_date = current_date - timedelta(days=for_which_day)
			exp_end_date = current_date - timedelta(days=for_which_day)

			task.exp_start_date = exp_start_date.strftime('%Y-%m-%d')
			task.exp_end_date = exp_end_date.strftime('%Y-%m-%d')

			task.save()

			# Move to the next date
			current_date += timedelta(days=1)

		# Display a message indicating the tasks were created
		frappe.msgprint(f"Updated tasks for {self.name}")

	def update_tasks_for_custom_days(self):
		# Get start and end dates
		start_date = datetime.strptime(self.actual_start_date, '%Y-%m-%d').date()
		end_date = datetime.strptime(self.actual_end_date, '%Y-%m-%d').date()

		# Check if both start and end dates are set
		if not (start_date and end_date):
			frappe.msgprint("Please set both Actual Start Date and Actual End Date.")
			return
		
		# Get the selected days from the repeat_on_days property
		selected_days = [day.day for day in self.repeat_on_days]
		# Convert for_which_day to integer
		for_which_day = int(self.for_which_day)

		current_date = start_date
		while current_date <= end_date:
			# Check if the current day is in the list of selected days
			if current_date.strftime('%A') in selected_days:
				# Check if task already exists for this date
				existing_task = frappe.get_all("Task", filters={"subject": f"{self.subject} for {formatdate(current_date, 'dd MMMM')}"})
				if existing_task:
					task = frappe.get_doc("Task", existing_task[0].name)
				else:
					task = frappe.new_doc("Task")

				# Set the subject and project for the task
				task.subject = f"{self.subject} for {formatdate(current_date, 'dd MMMM')}"
				task.project = self.project

				# Calculate the exp_start_date and exp_end_date
				exp_start_date = current_date - timedelta(days=for_which_day)
				exp_end_date = current_date - timedelta(days=for_which_day)

				task.exp_start_date = exp_start_date.strftime('%Y-%m-%d')
				task.exp_end_date = exp_end_date.strftime('%Y-%m-%d')

				# Save the task document
				task.save()

			# Move to the next date
			current_date += timedelta(days=1)

		# Display a message indicating the tasks were created
		frappe.msgprint(f"Updated tasks for {self.name}")
