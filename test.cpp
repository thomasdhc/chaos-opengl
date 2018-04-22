// Include standard headers
#include <stdio.h>
#include <stdlib.h>
#include <vector>

// Include GLEW
#include <GL/glew.h>

// Include GLFW
#include <GLFW/glfw3.h>
GLFWwindow* window;

// Include GLM
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
using namespace glm;

#include "common/shader.hpp"
#include "common/controls.hpp"

void generateVertices(
	std::vector<vec3> &finalVertices
){
	std::vector<std::vector<vec3> > verticesList;
	GLfloat currentR = 2.4;

	GLint duration = 20;
	GLint rIteration = 20;

	for (int z = 0; z < rIteration; z++){
		std::vector<vec3> currentArray;
		GLfloat step = 0.0;
		GLfloat currentPopulation = 0.1;
		GLfloat newPopulation;
		for (int x = 0; x < duration; x++){
			vec3 vertex = vec3(step, currentPopulation * 10.0f, currentR);
			currentArray.push_back(vertex);
			newPopulation = currentR * currentPopulation * (1 - currentPopulation);
			currentPopulation = newPopulation;
			step = step + 1.0;
		}
		verticesList.push_back(currentArray);
		currentR = currentR + 0.1;
	}

	for (int z = 0; z < rIteration - 1; z++){
		std::vector<vec3> vertices1 = verticesList[z];
		std::vector<vec3> vertices2 = verticesList[z + 1];

		for (int x = 0; x < duration; x++) {
			if (x % 2 == 0){
				if (x != 0){
					finalVertices.push_back(vertices2[x]);
					finalVertices.push_back(vertices1[x - 1]);
					finalVertices.push_back(vertices1[x]);
				}

				if (x != duration - 1) {
					finalVertices.push_back(vertices2[x]);
					finalVertices.push_back(vertices1[x]);
					finalVertices.push_back(vertices1[x + 1]);
				}
			} else {
				if (x != 0){
					finalVertices.push_back(vertices1[x]);
					finalVertices.push_back(vertices2[x - 1]);
					finalVertices.push_back(vertices2[x]);
				}

				if (x != duration - 1) {
					finalVertices.push_back(vertices1[x]);
					finalVertices.push_back(vertices2[x]);
					finalVertices.push_back(vertices2[x + 1]);
				}
			}
		}
	}
}

void windowInitlization(){
	glfwInit();

	glfwWindowHint(GLFW_SAMPLES, 4);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

	window = glfwCreateWindow(1024, 768, "chaos-opengl", NULL, NULL);
	glfwMakeContextCurrent(window);

	// Initialize GLEW
	glewExperimental = true; // Needed for core profile
	glewInit();

	// Detect escape key
	glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);
	// Hide mouse and enable unlimited movement
	glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
	glfwPollEvents();
	glfwSetCursorPos(window, 1024/2, 768/2);

	// Background color
	glClearColor(0.0f, 0.0f, 0.4f, 0.0f);

	// Enable Depth
	glEnable(GL_DEPTH_TEST);
	glDepthFunc(GL_LESS);
	// Do not display triangles not in vision of camera
	// glEnable(GL_CULL_FACE);
}

int main(){

	windowInitlization();

	GLuint VertexArrayID;
	glGenVertexArrays(1, &VertexArrayID);
	glBindVertexArray(VertexArrayID);

	// Create and compile our GLSL program from the shaders
	GLuint programID = LoadShaders("TransformVertexShader.glsl", "ColorFragmentShader.glsl");
	GLuint MatrixID = glGetUniformLocation(programID, "MVP");

	std::vector<vec3> vertexVector;
	generateVertices(vertexVector);

	GLfloat g_vertex_buffer_data[vertexVector.size() * 3];
	GLfloat g_color_buffer_data[vertexVector.size() * 3];

	GLfloat r1 = 1.0f;
	GLfloat g1 = 0.0f;
	GLfloat b1 = 0.0f;
	GLfloat r2 = 0.0f;
	GLfloat g2 = 1.0f;
	GLfloat b2 = 0.0f;
	int colorSet = 0;

	for (int x = 0; x < vertexVector.size(); x ++){
		GLfloat r, g, b;
		if (colorSet == 1){
			r = r1;
			g = g1;
			b = b1;
		} else {
			r = r2;
			g = g2;
			b = b2;
		}

		g_vertex_buffer_data[x * 3] = vertexVector[x].x;
		g_vertex_buffer_data[x * 3 + 1] = vertexVector[x].y;
		g_vertex_buffer_data[x * 3 + 2] = vertexVector[x].z;

		g_color_buffer_data[x * 3] = r;
		g_color_buffer_data[x * 3 + 1] = g;
		g_color_buffer_data[x * 3 + 2] = b;
		if (x % 3 == 2){
			colorSet = colorSet == 0 ? 1 : 0;
		}
	}

	GLuint vertexbuffer;
	glGenBuffers(1, &vertexbuffer);
	glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);
	glBufferData(GL_ARRAY_BUFFER, sizeof(g_vertex_buffer_data), g_vertex_buffer_data, GL_STATIC_DRAW);

	GLuint colorbuffer;
	glGenBuffers(1, &colorbuffer);
	glBindBuffer(GL_ARRAY_BUFFER, colorbuffer);
	glBufferData(GL_ARRAY_BUFFER, sizeof(g_color_buffer_data), g_color_buffer_data, GL_STATIC_DRAW);

	do {
		// Clear the screen
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		glUseProgram(programID);

		computeMatricesFromInputs();
		glm::mat4 ProjectionMatrix = getProjectionMatrix();
		glm::mat4 ViewMatrix = getViewMatrix();
		glm::mat4 ModelMatrix = glm::mat4(1.0);
		glm::mat4 MVP = ProjectionMatrix * ViewMatrix * ModelMatrix;

		glUniformMatrix4fv(MatrixID, 1, GL_FALSE, &MVP[0][0]);

		// vertex buffer
		glEnableVertexAttribArray(0);
		glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);
		glVertexAttribPointer(
			0,
			3,
			GL_FLOAT,
			GL_FALSE,
			0,
			(void*)0
		);

		// color buffer
		glEnableVertexAttribArray(1);
		glBindBuffer(GL_ARRAY_BUFFER, colorbuffer);
		glVertexAttribPointer(
			1,
			3,
			GL_FLOAT,
			GL_FALSE,
			0,
			(void*)0
		);

		glDrawArrays(GL_TRIANGLES, 0, vertexVector.size());

		glDisableVertexAttribArray(0);
		glDisableVertexAttribArray(1);

        glfwSwapBuffers(window);
		glfwPollEvents();

	} while(glfwGetKey(window, GLFW_KEY_ESCAPE) != GLFW_PRESS &&
		   glfwWindowShouldClose(window) == 0);

	glDeleteBuffers(1, &vertexbuffer);
	glDeleteBuffers(1, &colorbuffer);
	glDeleteProgram(programID);
	glDeleteVertexArrays(1, &VertexArrayID);

	glfwTerminate();

	return 0;
}