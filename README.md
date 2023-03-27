# 1. Water Treatment Digital Twin 
## 1.1 Index
- [Overview](#12-overview)
- [C/D](#121-continuous-deployment)
- [Planning](#13-planning)
- [Stakeholders](#14-stakeholders)
- [User stories](#15-user-stories)
- [Development and Depolyment](#16-development-and-deployment)
- [Styling](#17-styling)
- [Links](#18-kanban-gantt-chart-preview) to Kanban Board, Gantt Chart and Site Preview 
---
## 1.2 Overview
> _Nijhuis Saur Industries provides solid and adaptive solutions for sustainable and resilient water use, energy and resource recovery around the world._ - [Nijhuis Industries](https://www.nijhuisindustries.com/)

Water treatment plants need a tool which can help improve the planning, design, contruction and operation of their plants. 
A digital twin of a water system will provide accurate and reliable data of that can used to make informed decisions throughout 
the lifecycle of that water system. \
This will consist of: 
  - A front-end in Django + HTML Templates. 
  - A backend in Django + pyRevit to interface with Revit APIs.

## 1.2.1 Continuous Deployment (C/D)
C/D has been configured using Google Cloud Build triggers. This listens on the main branch. During every commit, a Docker image is built, 
pushes to the Google Cloud repository. The application is then built using the latest Docker image. Click the link below to view the web application. 
  - https://beta-release-vb27oaoulq-ew.a.run.app

## 1.3 Planning

Main planned features include:
- 3D modelling of plant details, similar to tools like Revit.
- Ability to simulate running process of a plant designed in the software.
- Ability to connect the software to a live system to allow for updates to the model from the real world.
  - Including visual updates to the 3D model.
- Ability to use the software to control real world components.


## 1.4 Stakeholders
- John Williams
- Nijhuis Industries
  - Employees
  - Shareholders
- Nijhuis Clients
  - Public Sector
  - Private Sector


## 1.5 User stories
- As John Williams, I want to improve the design tools for water treatment plants, so that I can design better plants.
- As a Nijhuis Employee, I want to have better design tools, so that the design process can be easier and more accurate.
- As a Nijhuis Shareholder, I want to improve the efficiency and turnaround speed on plant designs, so that the company is able to generate more business.
- As a public sector Nijhuis client, I want to have more effetive treatment plants with better control tools, so that water treatment can be more effective to reduce costs.
- As a private sectore Nijhuis client, I want to take advantage of waste water produced at my factories, so that my business is more profitable.
  

 ## 1.6 Development and Deployment
 [Starting the Frontend](https://github.com/spe-uob/2022-WaterTreatmentDigitalTwin/blob/main/django/README.md) \
 [Starting the Backend](https://github.com/spe-uob/2022-WaterTreatmentDigitalTwin/blob/main/src/README.md)
 
 ## 1.7 Styling
 We are following [Google Style Guides](https://google.github.io/styleguide/) for our code:
 - [Python](https://google.github.io/styleguide/pyguide.html) 
 - [JavaScript](https://google.github.io/styleguide/jsguide.html) 
 - [HTML/CSS](https://google.github.io/styleguide/htmlcssguide.html) 
 
 We also frequently refer to [Django's](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/) official docs for their conventions.
 
We attempt to keep our code **clean** and **understandable** while following these standards. \
We adopted these conventions so that our code is *consistent*. \
Others can then focus on what we're saying rather than how we are trying to say it.
 
  ## 1.8 Kanban, Gantt Chart, Preview 
  [Kanban](https://github.com/spe-uob/2022-WaterTreatmentDigitalTwin/projects/1) \
  [Gantt Chart](https://uob-my.sharepoint.com/:x:/g/personal/ij21409_bristol_ac_uk/EX73IxO8MzxJpIT4n8v2akIBD4Ke-R7LHc50kl0CKyK-Aw?e=IhAzEd) \
  [Preview](https://github.com/spe-uob/2022-WaterTreatmentDigitalTwin/blob/main/django/PREVIEW.md)

<p align="right">[<a href="#11-index">Top</a>]</p>
