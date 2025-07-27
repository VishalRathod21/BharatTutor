class NCERTKnowledgeBase:
    def __init__(self):
        """Initialize NCERT knowledge base with sample content."""
        self.knowledge_base = self._create_sample_knowledge_base()
    
    def _create_sample_knowledge_base(self) -> dict:
        """Create a sample knowledge base with NCERT content structure."""
        return {
            "Mathematics": {
                "Class 6": {
                    "topics": [
                        "Knowing Our Numbers", "Whole Numbers", "Playing with Numbers",
                        "Basic Geometrical Ideas", "Understanding Elementary Shapes",
                        "Integers", "Fractions", "Decimals", "Data Handling", "Mensuration",
                        "Algebra", "Ratio and Proportion", "Symmetry", "Practical Geometry"
                    ],
                    "content": {
                        "Fractions": "Fractions represent parts of a whole. A fraction has a numerator (top number) and denominator (bottom number). Example: 1/2 means one part out of two equal parts.",
                        "Integers": "Integers include positive numbers, negative numbers, and zero. They are represented on a number line extending infinitely in both directions.",
                        "Basic Geometrical Ideas": "Geometry deals with points, lines, angles, and shapes. A point has no dimension, a line extends infinitely in both directions, and angles are formed when two lines meet."
                    }
                },
                "Class 7": {
                    "topics": [
                        "Integers", "Fractions and Decimals", "Data Handling", "Simple Equations",
                        "Lines and Angles", "The Triangle and its Properties", "Congruence of Triangles",
                        "Comparing Quantities", "Rational Numbers", "Practical Geometry",
                        "Perimeter and Area", "Algebraic Expressions", "Exponents and Powers", "Symmetry"
                    ],
                    "content": {
                        "Simple Equations": "An equation is a statement that two expressions are equal. Solving equations means finding the value of the variable that makes the equation true.",
                        "Rational Numbers": "Rational numbers are numbers that can be expressed as p/q where p and q are integers and q ≠ 0."
                    }
                }
            },
            "Science": {
                "Class 6": {
                    "topics": [
                        "Food: Where Does it Come From?", "Components of Food", "Fibre to Fabric",
                        "Sorting Materials into Groups", "Separation of Substances", "Changes Around Us",
                        "Getting to Know Plants", "Body Movements", "The Living Organisms and Their Surroundings",
                        "Motion and Measurement of Distances", "Light, Shadows and Reflections",
                        "Electricity and Circuits", "Fun with Magnets", "Water", "Air Around Us", "Garbage In, Garbage Out"
                    ],
                    "content": {
                        "Photosynthesis": "Photosynthesis is the process by which green plants make their own food using sunlight, carbon dioxide, and water. Chlorophyll in leaves captures sunlight energy.",
                        "Water Cycle": "Water cycle is the continuous movement of water on Earth through evaporation, condensation, and precipitation."
                    }
                },
                "Class 10": {
                    "topics": [
                        "Chemical Reactions and Equations", "Acids, Bases and Salts", "Metals and Non-metals",
                        "Carbon and its Compounds", "Periodic Classification of Elements", "Life Processes",
                        "Control and Coordination", "How do Organisms Reproduce?", "Heredity and Evolution",
                        "Light - Reflection and Refraction", "The Human Eye and Colourful World",
                        "Electricity", "Magnetic Effects of Electric Current", "Our Environment", "Management of Natural Resources"
                    ],
                    "content": {
                        "Acids and Bases": "Acids are substances that release H+ ions in aqueous solution. Bases are substances that release OH- ions. pH scale measures acidity and basicity from 0-14.",
                        "Periodic Table": "Elements are arranged in periodic table based on increasing atomic number. Elements in same group have similar properties."
                    }
                }
            },
            "Social Science": {
                "Class 6": {
                    "topics": [
                        "What, Where, How and When?", "From Hunting-Gathering to Growing Food",
                        "In the Earliest Cities", "What Books and Burials Tell Us", "Kingdoms, Kings and an Early Republic",
                        "New Questions and Ideas", "Ashoka, The Emperor Who Gave Up War"
                    ],
                    "content": {
                        "Indus Valley Civilization": "The Harappan civilization flourished around 2600-1900 BCE in the Indus Valley. They had well-planned cities with drainage systems.",
                        "Mauryan Empire": "Founded by Chandragupta Maurya, the Mauryan Empire was one of the largest empires in ancient India. Ashoka was its most famous ruler."
                    }
                }
            },
            "English": {
                "Class 6": {
                    "topics": [
                        "Grammar: Nouns, Pronouns, Verbs", "Reading Comprehension", "Creative Writing",
                        "Poetry Analysis", "Story Writing", "Letter Writing"
                    ],
                    "content": {
                        "Parts of Speech": "Nouns name people, places, or things. Verbs show action or state of being. Adjectives describe nouns.",
                        "Reading Comprehension": "Understanding what you read involves identifying main ideas, supporting details, and making inferences."
                    }
                }
            },
            "Hindi": {
                "Class 6": {
                    "topics": [
                        "व्याकरण", "गद्य", "पद्य", "रचना", "पत्र लेखन"
                    ],
                    "content": {
                        "व्याकरण": "हिंदी व्याकरण में संज्ञा, सर्वनाम, विशेषण, क्रिया आदि शब्द भेद हैं।",
                        "गद्य": "गद्य साहित्य में कहानी, निबंध, नाटक आदि विधाएं आती हैं।"
                    }
                }
            }
        }
    
    def get_relevant_content(self, query: str, subject: str, class_level: str) -> str:
        """Get relevant content from knowledge base based on query, subject, and class."""
        try:
            # Get subject content for the specified class
            subject_content = self.knowledge_base.get(subject, {})
            class_content = subject_content.get(class_level, {})
            content_dict = class_content.get("content", {})
            topics_list = class_content.get("topics", [])
            
            # Simple keyword matching for relevant content
            query_lower = query.lower()
            relevant_content = []
            
            # Check if query matches any topic content
            for topic, content in content_dict.items():
                if any(word in topic.lower() for word in query_lower.split()) or \
                   any(word in content.lower() for word in query_lower.split()):
                    relevant_content.append(f"Topic: {topic}\nContent: {content}")
            
            # If no specific content found, provide topic list
            if not relevant_content:
                topics_str = ", ".join(topics_list[:10])  # First 10 topics
                relevant_content.append(f"Available topics in {subject} {class_level}: {topics_str}")
            
            return "\n\n".join(relevant_content) if relevant_content else f"Content for {subject} {class_level} is being updated."
            
        except Exception as e:
            return f"Error retrieving content: {str(e)}"
    
    def get_topics_for_subject_class(self, subject: str, class_level: str) -> list:
        """Get list of topics for a specific subject and class."""
        try:
            return self.knowledge_base.get(subject, {}).get(class_level, {}).get("topics", [])
        except Exception:
            return []
    
    def add_content(self, subject: str, class_level: str, topic: str, content: str):
        """Add new content to the knowledge base."""
        try:
            if subject not in self.knowledge_base:
                self.knowledge_base[subject] = {}
            
            if class_level not in self.knowledge_base[subject]:
                self.knowledge_base[subject][class_level] = {"topics": [], "content": {}}
            
            # Add topic to topics list if not already present
            if topic not in self.knowledge_base[subject][class_level]["topics"]:
                self.knowledge_base[subject][class_level]["topics"].append(topic)
            
            # Add content
            self.knowledge_base[subject][class_level]["content"][topic] = content
            
        except Exception as e:
            print(f"Error adding content: {e}")
