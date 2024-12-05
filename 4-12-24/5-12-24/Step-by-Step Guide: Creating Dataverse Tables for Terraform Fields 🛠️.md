### Step-by-Step Guide: Creating Dataverse Tables for Terraform Fields 🛠️

---

### **🌟 Purpose**
To structure Terraform variables (including maps, objects, and optional fields) into Dataverse tables while dynamically handling nested relationships between fields, ensuring proper navigation, input validation, and extendability.

---

### **📝 Task at Hand**
1. Create **two Dataverse tables**:
   - **TerraformVariables**: To store all fields (including nested ones) and their metadata.
   - **TerraformMappings**: To link parent fields (wrappers) to their child fields.
2. Populate these tables with data such as field type, optionality, default values, and parent-child relationships.
3. Ensure the hierarchy of nested objects is maintained for dynamic management in Dataverse.

---

### **📋 Desired Results**
1. **Flat Structure**: Each field is stored as a single row in **TerraformVariables** with clear metadata.
2. **Hierarchical Relationships**: Parent-child relationships are stored in **TerraformMappings**.
3. **Dynamic Navigation**: Support for deeply nested maps and objects.
4. **Input Validation**: Ensure fields follow Terraform syntax for types and optionality.

---

### **🚀 Step-by-Step Instructions**

---

#### **Step 1: Set Up the Tables in Dataverse**

1. **📂 Create `TerraformVariables` Table**:
   - **Columns**:
     - `VariableName` (Text): Name of the main Terraform variable (e.g., `Storage_Account`).
     - `FieldName` (Text): Name of the current field (e.g., `blob_properties` or `allowed_headers`).
     - `FieldType` (Choice): Type of the field (`object`, `map`, `string`, `list`, etc.).
     - `IsOptional` (Yes/No): Whether the field is optional.
     - `ParentField` (Lookup): References the parent field (e.g., `blob_properties` for `cors_rule`).
     - `DefaultValue` (Text): The default value for the field if defined.
     - `IsWrapper` (Yes/No): Whether the field is a wrapper for nested fields.
     - `Description` (Text): Description or purpose of the field.

2. **📂 Create `TerraformMappings` Table**:
   - **Columns**:
     - `ParentField` (Lookup): The parent wrapper field.
     - `ChildField` (Lookup): The child field within the parent wrapper.
     - `WrapperType` (Choice): The type of the wrapper (`object`, `map`, or `optional`).
     - `IndentLevel` (Number): The level of the child field within the parent hierarchy.
     - `FieldType` (Choice): Type of the child field.

---

#### **Step 2: Extract Data from Terraform Code**

1. **📊 Parse Flat Rows**:
   - Use a parser to flatten the Terraform code into rows. 
   - Include columns for:
     - `FieldName`
     - `FieldType`
     - `IsOptional`
     - `IndentLevel`
     - `ParentField`
   - **Logic**:
     - Count spaces before each line to calculate `IndentLevel`.
     - Identify `FieldType` (e.g., `object`, `map`, `string`) based on syntax (`object(`, `map(`, etc.).
     - Set `ParentField` dynamically for nested fields by looking up the nearest field with a lower `IndentLevel`.

2. **🧹 Handle Wrappers**:
   - Identify fields starting with `object(`, `map(`, or `optional(` as wrappers.
   - Add a column `IsWrapper` to mark them as such.
   - Set their child fields' `ParentField` to the wrapper's `FieldName`.

---

#### **Step 3: Populate Dataverse Tables**

1. **📥 Populate `TerraformVariables`**:
   - Add all fields extracted in Step 2.
   - Include:
     - Top-level fields (e.g., `create_containers`).
     - Nested fields (e.g., `name`, `container_access_type`).
   - Set `ParentField` for child fields.

2. **📥 Populate `TerraformMappings`**:
   - For each wrapper, add a row linking it to its children:
     - `ParentField` → Wrapper (e.g., `create_containers`).
     - `ChildField` → Nested fields (e.g., `name`, `container_access_type`).
   - Specify:
     - `WrapperType`: Whether the parent is `object`, `map`, or `optional`.
     - `IndentLevel`: The nesting level of the child field.

---

#### **Step 4: Add Data Validation**

1. **✅ Ensure Field Validity**:
   - Check that:
     - All fields have a valid `FieldType`.
     - Optional fields are marked correctly (`IsOptional`).

2. **🔄 Handle Default Values**:
   - Parse default values from Terraform code (e.g., `optional(map(object()), null)`).
   - Populate `DefaultValue` column in `TerraformVariables`.

---

#### **Step 5: Link the Tables**

1. **🔗 Establish Relationships**:
   - Use `ParentField` to create hierarchical links in **TerraformMappings**.
   - Verify the integrity of relationships:
     - Each child field points to the correct parent.
     - Each wrapper correctly lists its children.

2. **🖇️ Enable Dynamic Navigation**:
   - In Dataverse, allow navigation between parents and children:
     - From `TerraformVariables`, view all child fields in `TerraformMappings`.
     - From `TerraformMappings`, view parent and child details.

---

#### **Step 6: Test and Validate**

1. **🔍 Test Cases**:
   - Add test variables such as `Storage_Account` and ensure:
     - Correct hierarchy for `create_containers` → `name`, `container_access_type`.
     - Correct linking for `blob_properties` → `cors_rule`.

2. **📈 Validate Output**:
   - Confirm:
     - All fields are correctly added to `TerraformVariables`.
     - Parent-child relationships are accurately reflected in `TerraformMappings`.

---

### **💡 Tips for Efficient Execution**
1. **Use Power Automate**:
   - Automate table population by importing parsed rows into Dataverse.
2. **Leverage Hierarchical Views**:
   - Use Dataverse's native hierarchical features to display parent-child relationships visually.
3. **Iterative Testing**:
   - Add one variable at a time and validate relationships before scaling up.

---

### **🎯 Final Outcome**
- A structured Dataverse setup that:
  - Dynamically handles `map(object)` and `object`.
  - Supports navigation and validation for deeply nested fields.
  - Enables efficient field management for Terraform variables.
