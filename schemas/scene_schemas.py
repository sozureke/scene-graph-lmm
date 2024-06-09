scene_schema = {
	"type": "object",
	"properties": {
		"image_name": { "type": "string" },
		"objects": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"id": { "type": "integer" },
					"name": { "type": "string" },
					"bounding_box": {
						"type": "object",
						"properties": {
							"x_min": { "type": "number" },
							"y_min": { "type": "number" },
							"x_max": { "type": "number" },
							"y_max": { "type": "number" }
						},
						"required": ["x_min", "y_min", "x_max", "y_max"]
					},
					"center": {
						"type": "object",
						"properties": {
							"x": { "type": "number" },
							"y": { "type": "number" }
						},
						"required": ["x", "y"]
					},
					"attributes": {
						"type": "object",
						"properties": {
							"color": { "type": "string" },
							"size": { "type": "string" },
							"position": { "type": "string" },
							"shape": { "type": "string" },
							"material": { "type": "string" },
							"orientation": { "type": "string" },
							"mass": { "type": "number" },
							"texture": { "type": "string" }
						},
						"required": [
							"color",
							"size",
							"position",
							"shape",
							"material",
							"orientation",
							"mass",
							"texture"
						]
					},
					"relations": {
						"type": "array",
						"items": {
							"type": "object",
							"properties": {
								"object_id": { "type": "integer" },
								"object_name": { "type": "string" },
								"relation_type": { "type": "string" },
								"relation_description": { "type": "string" },
								"relation_confidence": { "type": "number" }
							},
							"required": [
								"object_id",
								"object_name",
								"relation_type",
								"relation_description",
								"relation_confidence"
							]
						}
					},
					"semantic_context": {
						"type": "object",
						"properties": {
							"function": { "type": "string" },
							"actions": {
								"type": "array",
								"items": {
									"type": "object",
									"properties": {
										"action_name": { "type": "string" },
										"action_description": { "type": "string" }
									},
									"required": ["action_name", "action_description"]
								}
							}
						},
						"required": ["function", "actions"]
					}
				},
				"required": [
					"id",
					"name",
					"bounding_box",
					"center",
					"attributes",
					"relations",
					"semantic_context"
				]
			}
		}
	},
	"required": ["image_name", "objects"]
}
